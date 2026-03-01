"""
Data Models / Schemas

Defines the data structures used across the application.
These mirror the Supabase PostgreSQL table schemas and can be used
for validation and serialization.

Note: These are plain Python dataclasses — not ORM models.
The actual tables must be created in Supabase Dashboard or via SQL migrations.
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """Mirrors the 'users' table in Supabase."""
    id: str
    email: str
    full_name: str
    phone: str = ""
    role: str = "client"    # "client" or "lawyer"
    created_at: Optional[datetime] = None


@dataclass
class Lawyer:
    """
    Mirrors the 'lawyers' table in Supabase.

    This table stores lawyer-specific data for the matching system.
    Top-k relevant lawyers are retrieved by filtering on 'domain'
    and sorting by 'rating'.
    """
    user_id: str
    full_name: str
    email: str
    bar_registration: str
    portfolio_url: str = ""
    domain: str = ""            # e.g., "Tenancy & Property Law"
    location: str = ""          # e.g., "Mumbai"
    bio: str = ""
    rating: float = 0.0
    cases_handled: int = 0
    is_available: bool = True
    created_at: Optional[datetime] = None


@dataclass
class Document:
    """
    Mirrors the 'documents' table in Supabase.

    Status flow: draft → sent → completed
    """
    id: Optional[str] = None
    case_id: Optional[str] = None
    lawyer_id: str = ""
    client_id: Optional[str] = None
    title: str = ""
    content: str = ""
    document_type: str = ""     # "Legal Notice", "Appeal Letter", etc.
    status: str = "draft"       # "draft", "sent", "completed"
    notes: str = ""
    created_at: Optional[datetime] = None


@dataclass
class Consultation:
    """Mirrors the 'consultations' table in Supabase."""
    id: Optional[str] = None
    lawyer_id: str = ""
    client_id: str = ""
    case_id: Optional[str] = None
    message: str = ""
    preferred_date: Optional[str] = None
    status: str = "pending"     # "pending", "accepted", "declined", "completed"
    created_at: Optional[datetime] = None


# ── SQL Migration Reference ────────────────────────────────────
# Run these in the Supabase SQL Editor to create the tables:
#
# CREATE TABLE users (
#     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
#     email TEXT UNIQUE NOT NULL,
#     full_name TEXT NOT NULL,
#     phone TEXT DEFAULT '',
#     role TEXT CHECK (role IN ('client', 'lawyer')) DEFAULT 'client',
#     created_at TIMESTAMPTZ DEFAULT now()
# );
#
# CREATE TABLE lawyers (
#     user_id UUID PRIMARY KEY REFERENCES users(id),
#     full_name TEXT NOT NULL,
#     email TEXT NOT NULL,
#     bar_registration TEXT NOT NULL,
#     portfolio_url TEXT DEFAULT '',
#     domain TEXT DEFAULT '',
#     location TEXT DEFAULT '',
#     bio TEXT DEFAULT '',
#     rating FLOAT DEFAULT 0.0,
#     cases_handled INT DEFAULT 0,
#     is_available BOOLEAN DEFAULT true,
#     created_at TIMESTAMPTZ DEFAULT now()
# );
#
# CREATE TABLE documents (
#     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
#     case_id UUID,
#     lawyer_id UUID REFERENCES users(id),
#     client_id UUID REFERENCES users(id),
#     title TEXT NOT NULL,
#     content TEXT DEFAULT '',
#     document_type TEXT DEFAULT '',
#     status TEXT CHECK (status IN ('draft', 'sent', 'completed')) DEFAULT 'draft',
#     notes TEXT DEFAULT '',
#     created_at TIMESTAMPTZ DEFAULT now()
# );
#
# CREATE TABLE consultations (
#     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
#     lawyer_id UUID REFERENCES users(id),
#     client_id UUID REFERENCES users(id),
#     case_id UUID,
#     message TEXT DEFAULT '',
#     preferred_date DATE,
#     status TEXT CHECK (status IN ('pending', 'accepted', 'declined', 'completed'))
#         DEFAULT 'pending',
#     created_at TIMESTAMPTZ DEFAULT now()
# );
