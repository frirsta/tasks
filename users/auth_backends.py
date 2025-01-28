import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class Auth0JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return None

        try:
            token = auth_header.split()[1]
            payload = jwt.decode(
                token,
                settings.PUBLIC_KEY,
                algorithms=["RS256"],
                audience=settings.AUTH0_API_IDENTIFIER,
                issuer=settings.AUTH0_ISSUER
            )
            return payload, token
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f"Invalid token: {e}")
