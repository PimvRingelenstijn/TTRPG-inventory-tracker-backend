from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv

load_dotenv()

# Fetch Supabase connection variables
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")

# # Debug: Add this to see what's being read
# print(f"DEBUG - USER: {USER}")
# print(f"DEBUG - PASSWORD: {PASSWORD}")
# print(f"DEBUG - HOST: {HOST}")
# print(f"DEBUG - PORT: {PORT}")
# print(f"DEBUG - DBNAME: {DBNAME}")

# Construct the SQLAlchemy connection string for Supabase
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Create SQLAlchemy engine
# Note: If using Supabase Transaction Pooler or Session Pooler, use NullPool
# to disable SQLAlchemy client-side pooling (recommended for Supabase)
# For direct connection, you can use default pooling settings
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Use NullPool for Supabase connection pooling
    echo=False           # Set to True for SQL logging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def test_connection():
    """Test the database connection"""
    try:
        with engine.connect() as connection:
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return False


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
