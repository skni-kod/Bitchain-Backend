"""
URL mapping for crypto_reviews app.
"""
from django.urls import path

from django.urls import path
from .views import CryptoReviewView

app_name = 'crypto_reviews'

urlpatterns = [
    path('symbol/<str:symbol>/', CryptoReviewView.as_view(), name='crypto-review'),
]

