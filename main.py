from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import engine, get_db, Base, test_connection
from app.dbmodels import System  # Import dbmodels to register them with Base.metadata
from typing import List
import os

from app.routers import SystemRouter


# Create tables (only for development)
# In production, use Alembic migrations
def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)

app = FastAPI()

# Health check endpoint
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Startup event
@app.on_event("startup")
def startup():
    """Create database tables on startup"""
    # Test connection first
    if test_connection():
        print("Creating database tables...")
        create_tables()
        print("✅ Database tables created successfully!")
    else:
        print("⚠️  Warning: Database connection failed. Tables may not be created.")

app.include_router(SystemRouter.router, prefix="/system", tags=["systems"])