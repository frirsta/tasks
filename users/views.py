from django.db import IntegrityError
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .auth_backends import Auth0JWTAuthentication
from .serializers import UserSerializer
from .models import CustomUser


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


class ProfileView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class RegisterUserView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        username = data.get('username')
        profile_picture = data.get('profile_picture', None)
        bio = data.get('bio', "")

        if not email or not username:
            return Response({"error": "Email and username are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.create(
                email=email,
                username=username,
                profile_picture=profile_picture,
                bio=bio
            )

            user.set_unusable_password()
            user.save()

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response({"error": "A user with this email or username already exists"}, status=status.HTTP_400_BAD_REQUEST)
