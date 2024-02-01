"""
Views for the user API.
"""
import os.path
from django.conf import settings

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser


from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    UserImageSerializer
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user."""
        return self.request.user


class UpdateUserImageView(APIView):
    """Manage the authenticated user."""
    serializer_class = UserImageSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser,)

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        absolute_path = os.path.abspath(os.path.join('..', settings.MEDIA_ROOT, user.image.name))

        file_exists = os.path.isfile(absolute_path)
        if file_exists and user.image.name != settings.DEFAULT_AVATAR_PATH:
            os.remove(absolute_path)  # Remove the custom image file
            user.image.name = settings.DEFAULT_AVATAR_PATH
            
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
