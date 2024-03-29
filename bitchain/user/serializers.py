"""
Serializers for the user API VIEW.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from rest_framework import serializers

from core.models import (
    FavoriteUserCryptocurrency,
    UserFundTransaction,
    UserWalletOverview,
    UserFundWallet,
    UserFundWalletCryptocurrency,
)


from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    @staticmethod
    def validate_pesel(value):
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

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it."""
        password = validated_data.pop('password', None)

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class UserImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to users"""
    class Meta:
        model = get_user_model()
        fields = ('image',)

    def update(self, instance, validated_data):
        """Update a user, setting the image correctly and return it."""
        image = validated_data.pop('image', None)

        user = super().update(instance, validated_data)

        if image:
            user.image = image
            user.save()
        return user


class FavoriteUserCryptocurrencySerializer(serializers.ModelSerializer):
    """Serializer for favorite user cryptocurrency objects."""
    class Meta:
        model = FavoriteUserCryptocurrency
        fields = ('favorite_crypto_symbol',)
      
        
class UserFundTransactionSerializer(serializers.ModelSerializer):
    """Serializer for user fund transaction objects. """
    
    class Meta:
        model = UserFundTransaction
        fields = ('transaction_id',
                  'transaction_type',
                  'transaction_amount',
                  'transaction_price_usd',
                  'transaction_currency',
                  'transaction_date')

        read_only_fields = ('transaction_id', 'transaction_date')
        
    def save(self, user):
        """Save the user fund transaction."""
        transaction = UserFundTransaction.objects.create(
            fund_wallet=UserFundWallet.objects.get(fund_wallet=UserWalletOverview.objects.get(user=user)),
            transaction_type=self.validated_data['transaction_type'],
            transaction_amount=self.validated_data['transaction_amount'],
            transaction_price_usd=self.validated_data['transaction_price_usd'],
            transaction_currency=self.validated_data['transaction_currency'],
        )
        return transaction
    

class UserFundWalletCryptoSerializer(serializers.ModelSerializer):
    """Serializer for user fund wallet cryptocurrency objects."""
    class Meta:
        model = UserFundWalletCryptocurrency
        fields = ('cryptocurrency_symbol', 'cryptocurrency_amount')
        
    def update(self, instance, validated_data):
        symbol = validated_data['cryptocurrency_symbol']
        amount_change = validated_data['cryptocurrency_amount']

        if amount_change < 0 and instance.cryptocurrency_amount < abs(amount_change):
            raise serializers.ValidationError({"error": "Not enough cryptocurrency to make the transaction."})

        instance.cryptocurrency_amount += amount_change
        instance.save()
        return instance