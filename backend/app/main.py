from fastapi import FastAPI
from sqlalchemy import text

from backend.app.database.database import engine


app = FastAPI(
    title="AI Disaster Management Platform",
    description="Backend API for the AI Disaster Management Platform",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "AI Disaster Management Platform API is running"
    }


@app.get("/health")
def health():
    return {
        "success": True,
        "status": "healthy"
    }


@app.get("/health/database")
def database_health():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT current_database()"))
            database_name = result.scalar()

        return {
            "success": True,
            "database": database_name,
            "status": "connected"
        }

    except Exception as e:
        return {
            "success": False,
            "status": "disconnected",
            "error": str(e)
        }