"""
Shared utility functions for the Adaalat backend.
"""

import re
from datetime import datetime


def classify_legal_domain(text):
    """
    Classify a legal query into a domain based on keyword matching.

    This is a lightweight fallback classifier used when the LLM
    hasn't been configured yet.

    Args:
        text: The legal query text

    Returns:
        str: The classified legal domain
    """
    text_lower = text.lower()

    domain_keywords = {
        "Tenancy & Property Law": [
            "tenant", "landlord", "rent", "eviction", "lease", "property",
            "housing", "accommodation", "premises",
        ],
        "Employment & Labour Law": [
            "employ", "job", "fired", "termination", "salary", "workplace",
            "harassment", "labour", "labor", "worker",
        ],
        "Family & Matrimonial Law": [
            "divorce", "custody", "marriage", "alimony", "domestic",
            "child", "spouse", "maintenance",
        ],
        "Consumer Protection": [
            "consumer", "product", "refund", "defective", "warranty",
            "complaint", "service", "seller",
        ],
        "Cyber Crime & IT Law": [
            "cyber", "online", "fraud", "hacking", "phishing", "internet",
            "digital", "data", "privacy", "identity theft",
        ],
        "Criminal Law": [
            "criminal", "theft", "assault", "murder", "robbery", "cheating",
            "forgery", "bail", "arrest", "fir",
        ],
        "Civil Law": [
            "civil", "dispute", "agreement", "contract", "breach",
            "damages", "compensation", "injunction",
        ],
    }

    for domain, keywords in domain_keywords.items():
        if any(kw in text_lower for kw in keywords):
            return domain

    return "General Law"


def sanitize_input(text):
    """
    Sanitize user input by removing potentially harmful content.

    Args:
        text: Raw input string

    Returns:
        str: Sanitized string
    """
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def format_timestamp(dt=None):
    """
    Format a datetime to ISO 8601 string.

    Args:
        dt: datetime object (defaults to now)

    Returns:
        str: Formatted timestamp
    """
    if dt is None:
        dt = datetime.utcnow()
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
