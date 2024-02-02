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

from drf_spectacular.utils import extend_schema

from core.models import FavoriteUserCryptocurrency

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    UserImageSerializer,
    FavoriteUserCryptocurrencySerializer,
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
        
    
class FavoriteUserCryptocurrencyView(APIView):
    """View for managing user's favorite cryptocurrencies."""

    serializer_class = FavoriteUserCryptocurrencySerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


    def get(self, request, *args, **kwargs):
        user = self.request.user
        favorites = FavoriteUserCryptocurrency.objects.filter(user=user)
        symbols = [favorite.favorite_crypto_symbol for favorite in favorites]
        favorites = {"favorite_crypto_symbol": symbols}
        return Response(favorites, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        try:
            # Delete all FavoriteUserCryptocurrency objects for the current user
            FavoriteUserCryptocurrency.objects.filter(user=request.user).delete()

            # Retrieve the list of favorite cryptocurrencies from the request
            favorite_crypto_list = request.data.get('favorite_crypto_symbol', [])

            # Add new favorite cryptocurrencies
            for crypto_symbol in favorite_crypto_list:
                FavoriteUserCryptocurrency.objects.create(user=request.user, favorite_crypto_symbol=crypto_symbol)

            updated_favorites = list(FavoriteUserCryptocurrency.objects.filter(user=request.user))
            serializer = self.serializer_class(updated_favorites, many=True)

            return Response({'success': True, 'message': 'Favorites updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
