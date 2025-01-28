from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def root_route(request):
    """
    Provides a welcome message and documentation link for the API.
    """
    return Response({
        "message": "Welcome to the Tasks API!",
        "description": (
            "This is the backend API for the tasks management platform, providing endpoints for"
        ),
    })
