"""
Authentication Service
Handles user registration and login via Supabase Auth + PostgreSQL.
"""

from database.supabase_client import get_supabase_client


class AuthService:

    @staticmethod
    def signup(data):
        """
        Register a new user in Supabase Auth and store profile in PostgreSQL.

        For lawyers, also stores bar registration number and portfolio URL
        in the 'lawyers' table for later matching.

        Args:
            data: dict with email, password, fullName, phone, role,
                  and optionally barRegistration, portfolioUrl

        Returns:
            (result_dict, None) on success
            (None, error_string) on failure
        """
        try:
            supabase = get_supabase_client()

            # 1. Create auth user in Supabase Auth
            auth_response = supabase.auth.sign_up({
                "email": data["email"],
                "password": data["password"],
                "options": {
                    "data": {
                        "full_name": data["fullName"],
                        "role": data["role"],
                    }
                }
            })

            user = auth_response.user
            if not user:
                return None, "Failed to create user"

            # 2. Insert user profile in 'users' table
            profile = {
                "id": user.id,
                "email": data["email"],
                "full_name": data["fullName"],
                "phone": data.get("phone", ""),
                "role": data["role"],
            }
            supabase.table("users").insert(profile).execute()

            # 3. If lawyer, insert into 'lawyers' table
            if data["role"] == "lawyer":
                lawyer_profile = {
                    "user_id": user.id,
                    "bar_registration": data["barRegistration"],
                    "portfolio_url": data.get("portfolioUrl", ""),
                    "full_name": data["fullName"],
                    "email": data["email"],
                    "domain": "",           # To be updated by lawyer later
                    "location": "",         # To be updated by lawyer later
                    "bio": "",              # To be updated by lawyer later
                    "rating": 0.0,
                    "cases_handled": 0,
                    "is_available": True,
                }
                supabase.table("lawyers").insert(lawyer_profile).execute()

            return {
                "user": {
                    "id": user.id,
                    "email": data["email"],
                    "fullName": data["fullName"],
                    "role": data["role"],
                },
                "token": auth_response.session.access_token if auth_response.session else None,
            }, None

        except Exception as e:
            return None, str(e)

    @staticmethod
    def login(email, password):
        """
        Authenticate user via Supabase Auth.

        Returns:
            (result_dict, None) on success
            (None, error_string) on failure
        """
        try:
            supabase = get_supabase_client()

            auth_response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password,
            })

            user = auth_response.user
            if not user:
                return None, "Invalid credentials"

            # Fetch user profile for role info
            profile = (
                supabase.table("users")
                .select("*")
                .eq("id", user.id)
                .single()
                .execute()
            )

            return {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "fullName": profile.data.get("full_name", ""),
                    "role": profile.data.get("role", "client"),
                },
                "token": auth_response.session.access_token if auth_response.session else None,
            }, None

        except Exception as e:
            return None, str(e)
