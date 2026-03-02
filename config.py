"""Shared global state for the application"""
# Standard library imports
from typing import Optional

# Third-party imports
from supabase import Client

# Global Supabase client (initialized in main.py-lifespan)
supabase_client: Optional[Client] = None
