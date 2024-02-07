from rest_framework import serializers
from .models import CryptoReview

class CryptoReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoReview
        fields = ['symbol', 'good', 'bad']