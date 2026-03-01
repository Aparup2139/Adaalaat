"""
Lawyer Service
Handles lawyer search, profile retrieval, and consultation booking.
Uses Supabase PostgreSQL for the lawyer registry.
"""

from database.supabase_client import get_supabase_client


class LawyerService:

    @staticmethod
    def search(domain="", location="", page=1, limit=10):
        """
        Search for lawyers by legal domain and/or location.

        Queries the 'lawyers' table in Supabase PostgreSQL.
        Top-k relevance matching by domain is done at the DB level.

        Args:
            domain: Legal area (e.g., "Tenancy & Property Law")
            location: City or region
            page: Page number (1-indexed)
            limit: Results per page

        Returns:
            (result_dict, None) on success
            (None, error_string) on failure
        """
        try:
            supabase = get_supabase_client()
            offset = (page - 1) * limit

            query = supabase.table("lawyers").select("*", count="exact")

            if domain:
                query = query.ilike("domain", f"%{domain}%")
            if location:
                query = query.ilike("location", f"%{location}%")

            query = query.eq("is_available", True)
            query = query.order("rating", desc=True)
            query = query.range(offset, offset + limit - 1)

            response = query.execute()

            lawyers = []
            for row in response.data:
                lawyers.append({
                    "id": row["user_id"],
                    "name": row["full_name"],
                    "domain": row["domain"],
                    "location": row.get("location", ""),
                    "rating": row.get("rating", 0),
                    "casesHandled": row.get("cases_handled", 0),
                    "barRegistration": row.get("bar_registration", ""),
                    "portfolioUrl": row.get("portfolio_url", ""),
                    "bio": row.get("bio", ""),
                    "isAvailable": row.get("is_available", True),
                })

            return {
                "lawyers": lawyers,
                "total": response.count or len(lawyers),
                "page": page,
            }, None

        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_profile(lawyer_id):
        """
        Retrieve a specific lawyer's full profile.

        Args:
            lawyer_id: The lawyer's user_id

        Returns:
            (lawyer_dict, None) on success
            (None, error_string) on failure
        """
        try:
            supabase = get_supabase_client()

            response = (
                supabase.table("lawyers")
                .select("*")
                .eq("user_id", lawyer_id)
                .single()
                .execute()
            )

            row = response.data
            if not row:
                return None, "Lawyer not found"

            return {
                "id": row["user_id"],
                "name": row["full_name"],
                "email": row.get("email", ""),
                "domain": row["domain"],
                "location": row.get("location", ""),
                "rating": row.get("rating", 0),
                "casesHandled": row.get("cases_handled", 0),
                "barRegistration": row.get("bar_registration", ""),
                "portfolioUrl": row.get("portfolio_url", ""),
                "bio": row.get("bio", ""),
                "isAvailable": row.get("is_available", True),
            }, None

        except Exception as e:
            return None, str(e)

    @staticmethod
    def book_consultation(lawyer_id, client_id, case_id=None, message="", preferred_date=None):
        """
        Create a consultation request from client to lawyer.

        Inserts a record in the 'consultations' table.

        Args:
            lawyer_id: Target lawyer's user_id
            client_id: Requesting client's user_id
            case_id: Optional case reference
            message: Client's brief description
            preferred_date: Preferred consultation date

        Returns:
            (result_dict, None) on success
            (None, error_string) on failure
        """
        try:
            supabase = get_supabase_client()

            booking = {
                "lawyer_id": lawyer_id,
                "client_id": client_id,
                "case_id": case_id,
                "message": message,
                "preferred_date": preferred_date,
                "status": "pending",
            }

            response = supabase.table("consultations").insert(booking).execute()

            return {
                "bookingId": response.data[0]["id"] if response.data else None,
            }, None

        except Exception as e:
            return None, str(e)
