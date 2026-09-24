import os

import jwt
from jwt import PyJWKClient

from dotenv import load_dotenv
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import UserProfile


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL is not configured in .env")


SUPABASE_ISSUER = f"{SUPABASE_URL}/auth/v1"
SUPABASE_JWKS_URL = f"{SUPABASE_ISSUER}/.well-known/jwks.json"

jwks_client = PyJWKClient(SUPABASE_JWKS_URL)


class SupabaseAuthentication(BaseAuthentication):

    def authenticate(self, request):

        auth_header = request.headers.get("Authorization")

        print("AUTH HEADER PRESENT:", bool(auth_header))

        if not auth_header:
            return None

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise AuthenticationFailed(
                "Invalid Authorization header."
            )

        token = parts[1]

        try:
            signing_key = jwks_client.get_signing_key_from_jwt(token)

            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["ES256", "RS256"],
                audience="authenticated",
                issuer=SUPABASE_ISSUER,
            )

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(
                "Supabase access token has expired."
            )

        except jwt.InvalidTokenError:
            raise AuthenticationFailed(
                "Invalid Supabase access token."
            )

        supabase_user_id = payload.get("sub")
        email = payload.get("email", "")

        if not supabase_user_id:
            raise AuthenticationFailed(
                "Supabase user ID is missing from token."
            )

        user_profile, created = UserProfile.objects.get_or_create(
            supabase_user_id=supabase_user_id,
            defaults={
                "email": email,
            },
        )

        if not created and email and user_profile.email != email:
            user_profile.email = email
            user_profile.save(update_fields=["email"])

        return (user_profile, None)