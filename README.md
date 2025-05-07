# Quran Word Analysis API

A FastAPI application that analyzes Arabic words to determine their morphological pattern (الوزن) and root verb (الفعل) using OpenAI's GPT-4 model.

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your OpenAI API key

## Running with Docker

```bash
docker build -t quran-word-analysis .
docker run -p 8088:8088 --env-file .env quran-word-analysis
```

## API Documentation

Once running, you can access:
- Swagger UI: http://localhost:8088/docs
- ReDoc: http://localhost:8088/redoc

## API Endpoints

### POST /api/v1/analyze

Analyzes an Arabic word and returns its morphological pattern and root verb.

Example request:
```json
{
    "word": "مسلمين"
}
```

Example response:
```json
{
    "الكلمة": "مسلمين",
    "الوزن": "مفعلين",
    "الفعل": "سلم"
}
``` 