from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import models
from database import engine, get_db, SessionLocal
from typing import List
import os

# Create tables (only for development)
# In production, use Alembic migrations
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

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

# Example CRUD endpoints
@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.post("/users")
async def create_user(email: str, full_name: str, db: Session = Depends(get_db)):
    user = models.User(email=email, full_name=full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Startup event
@app.on_event("startup")
async def startup():
    await create_tables()