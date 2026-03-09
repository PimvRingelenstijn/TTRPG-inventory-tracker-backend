# Standard library imports
import os
from contextlib import asynccontextmanager

# Third-party imports
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client

load_dotenv() # Load variables in .env

# Local imports
import config
from app.routers import auth_router, game_system_router
from db import Base, engine, test_connection


# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # === STARTUP ===
    print("Starting up...")

    # Test database connection
    if test_connection():
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    else:
        print("Warning: Database connection failed. Tables may not be created.")

    # Initialize Supabase client
    print("Initializing Supabase client...")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

    if not supabase_url or not supabase_key:
        print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env")
    else:
        config.supabase_client = create_client(supabase_url, supabase_key)
        print("Supabase client initialized successfully!")

    yield

    # === SHUTDOWN ===
    print("Shutting down...")
    if config.supabase_client:
        config.supabase_client = None
        print("Supabase client cleaned up")

app = FastAPI(lifespan=lifespan)

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

# Include routers below
app.include_router(
    auth_router,
    prefix="/mappers",
    tags=["authentication"]
)

app.include_router(
    game_system_router,
    prefix="/game-systems",
    tags=["game_systems"]
)
