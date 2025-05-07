from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import word_analysis
from app.core.config import settings
from app.services.openai_service import cleanup
import uvicorn

app = FastAPI(
    title="Quran Word Analysis API",
    description="API for analyzing Arabic words and their morphological patterns",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(word_analysis.router, prefix="/api/v1",
                   tags=["word-analysis"])


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup when the application shuts down."""
    await cleanup()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8088,
        reload=True  # Enable auto-reload during development
    )
