from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.word import WordRequest, WordAnalysis, BulkWordRequest, BulkWordAnalysis
from app.services.openai_service import analyze_word
import httpx
import asyncio
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/analyze", response_model=WordAnalysis)
async def analyze_single_word(
    word_request: WordRequest,
    background_tasks: BackgroundTasks
) -> WordAnalysis:
    """
    Analyze an Arabic word to get its morphological pattern and root verb.
    """
    try:
        result = await analyze_word(word_request.word, background_tasks)
        return result
    except Exception as e:
        logger.error(f"Error analyzing word: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/bulk", response_model=BulkWordAnalysis)
async def analyze_multiple_words(
    word_request: BulkWordRequest,
    background_tasks: BackgroundTasks
) -> BulkWordAnalysis:
    try:
        # Create tasks for all words
        tasks = [
            analyze_word(word, background_tasks)
            for word in word_request.words
        ]

        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results and handle any errors
        processed_results = []
        for word, result in zip(word_request.words, results):
            if isinstance(result, Exception):
                logger.error(f"Error analyzing word '{word}': {str(result)}")
                # Skip failed analyses
                continue
            processed_results.append(result)

        return BulkWordAnalysis(results=processed_results)
    except Exception as e:
        logger.error(f"Error in bulk analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
