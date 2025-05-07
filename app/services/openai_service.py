import logging
import httpx
from openai import AsyncOpenAI
from app.core.config import settings
from app.prompts import SYSTEM_PROMPT, get_analysis_prompt
import json
import socket
from fastapi import BackgroundTasks
import os
import asyncio

# Set up logging with more detail
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def clean_json_response(content: str) -> str:
    """Clean the response content by removing markdown code blocks."""
    # Remove markdown code blocks if present
    if content.startswith('```'):
        # Split by ``` and take the content between the first and last ```
        parts = content.split('```')
        if len(parts) >= 3:
            # If it's like ```json\n{...}\n```, take the middle part
            content = parts[1]
            # Remove the "json" or other language identifier if present
            if '\n' in content:
                content = content.split('\n', 1)[1]
    return content.strip()


# Clean and validate API key
api_key = settings.OPENAI_API_KEY.strip()  # Remove any whitespace
if not api_key.startswith('sk-'):
    raise ValueError("Invalid OpenAI API key format")

logger.info(f"API key validation: starts with 'sk-': {api_key.startswith('sk-')}")
logger.info(f"Using OpenAI model: {settings.OPENAI_MODEL}")


async def test_connectivity():
    """Test basic internet connectivity and DNS resolution."""
    try:
        # Test DNS resolution
        logger.info("Testing DNS resolution for api.openai.com...")
        ip = socket.gethostbyname('api.openai.com')
        logger.info(f"Successfully resolved api.openai.com to {ip}")

        # Test HTTPS connectivity
        logger.info("Testing HTTPS connectivity to OpenAI API...")
        async with httpx.AsyncClient(verify=True) as client:
            response = await client.get(
                'https://api.openai.com/v1/models',
                headers={'Authorization': f'Bearer {api_key}'},
                timeout=10.0
            )
            logger.info(f"OpenAI API connection test status: {response.status_code}")
        return True
    except socket.gaierror as e:
        logger.error(f"DNS resolution failed: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Connection test failed: {str(e)}")
        return False

# Log environment information
logger.info(f"Python version: {os.sys.version}")
logger.info(f"Environment variables set: OPENAI_API_KEY={'OPENAI_API_KEY' in os.environ}")
logger.info("Testing connectivity to OpenAI API...")

# Create async HTTP client
http_client = httpx.AsyncClient(
    timeout=httpx.Timeout(
        connect=10.0,
        read=30.0,
        write=30.0,
        pool=10.0
    ),
    verify=True,
    follow_redirects=True
)

# Initialize OpenAI client with cleaned API key
client = AsyncOpenAI(
    api_key=api_key,  # Use cleaned key
    http_client=http_client,
    timeout=30.0
)


async def analyze_word(word: str, background_tasks: BackgroundTasks = None) -> dict:
    """
    Analyze an Arabic word using OpenAI to get its morphological pattern and root verb.
    """
    try:
        logger.info(f"Starting analysis for word: {word}")
        logger.info("Making request to OpenAI API...")

        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": get_analysis_prompt(word)}
            ],
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS
        )

        content = response.choices[0].message.content.strip()
        logger.info(f"Raw response content: {content[:100]}...")

        # Clean the response content
        cleaned_content = clean_json_response(content)
        logger.info(f"Cleaned content: {cleaned_content}")

        try:
            result = json.loads(cleaned_content)
            logger.info(f"Successfully parsed JSON response: {result}")
            return result
        except json.JSONDecodeError as json_error:
            logger.error(f"Failed to parse JSON response: {str(json_error)}")
            logger.error(f"Invalid JSON content: {cleaned_content}")
            raise ValueError(f"Invalid JSON response from OpenAI: {str(json_error)}")

    except Exception as e:
        logger.error(f"Error analyzing word {word}: {str(e)}", exc_info=True)
        raise ValueError(f"Error analyzing word: {str(e)}")


async def cleanup():
    """Cleanup function to close the OpenAI client."""
    try:
        await http_client.aclose()
        logger.info("Successfully closed HTTP client")
    except Exception as e:
        logger.error(f"Error closing HTTP client: {str(e)}")

# Log initial setup completion
logger.info("OpenAI service initialization completed")
