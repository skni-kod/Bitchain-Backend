"""
Serializers for the user API VIEW.
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    def validate_pesel(self, value):
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("PESEL must be 11 digits and contain only numbers")
        return value

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'full_name', 'nick_name', 'date_of_birth', 'pesel')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it."""
        return get_user_model().objects.create_user(**validated_data)
