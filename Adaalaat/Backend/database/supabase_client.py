"""
Supabase Client

Initializes and provides a singleton Supabase client for PostgreSQL
database operations (user profiles, lawyer registry, documents, consultations).

Required environment variables:
    SUPABASE_URL — Your Supabase project URL
    SUPABASE_KEY — Your Supabase anon/service key

Supabase Tables Required:
    ┌─────────────────┐
    │     users        │  id, email, full_name, phone, role, created_at
    ├─────────────────┤
    │     lawyers      │  user_id (FK), bar_registration, portfolio_url,
    │                  │  full_name, email, domain, location, bio,
    │                  │  rating, cases_handled, is_available
    ├─────────────────┤
    │   documents      │  id, case_id, lawyer_id, client_id, title,
    │                  │  content, document_type, status, notes, created_at
    ├─────────────────┤
    │  consultations   │  id, lawyer_id, client_id, case_id,
    │                  │  message, preferred_date, status, created_at
    └─────────────────┘
"""

from config import Config

_supabase_client = None


def get_supabase_client():
    """
    Get or create the singleton Supabase client.

    Returns:
        supabase.Client — The initialized Supabase client

    Raises:
        ValueError if SUPABASE_URL or SUPABASE_KEY is not set
    """
    global _supabase_client

    if _supabase_client is None:
        if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_KEY must be set in .env. "
                "Get these from your Supabase project dashboard."
            )

        from supabase import create_client
        _supabase_client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

    return _supabase_client
