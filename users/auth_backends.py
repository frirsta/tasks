import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class JWTUser:
    def __init__(self, payload):
        self.payload = payload
        self.sub = payload.get("sub")
        self.email = payload.get("email")
        self.roles = payload.get("roles", [])

    @property
    def is_authenticated(self):
        return True


class Auth0JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", None)
        if not auth_header:
            return None

        try:
            token = auth_header.split()[1]

            payload = jwt.decode(
                token,
                settings.PUBLIC_KEY,
                algorithms=["RS256"],
                audience=settings.API_IDENTIFIER,
                issuer=settings.AUTH0_ISSUER
            )

            user = JWTUser(payload)
            return user, token

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f"Invalid token: {e}")
