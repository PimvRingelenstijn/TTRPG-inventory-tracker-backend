from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import engine, get_db, Base, test_connection
from app.routers import GameSystemRouter

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://localhost:3000",  # Alternative React port
        "http://127.0.0.1:5173",  # Sometimes localhost resolves to 127.0.0.1
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Create tables (only for development)
# In production, use Alembic migrations
def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)

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

app.include_router(GameSystemRouter.router, prefix="/game-systems", tags=["game_systems"])