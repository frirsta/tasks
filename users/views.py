from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .auth_backends import Auth0JWTAuthentication

class ProtectedView(APIView):
    authentication_classes = [Auth0JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "message": "You have access!",
            "user_email": user.email,
            "roles": user.roles,
        })
