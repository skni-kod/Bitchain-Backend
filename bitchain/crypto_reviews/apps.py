# crypto_reviews/apps.py
from django.apps import AppConfig

class CryptoReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crypto_reviews'

    def ready(self):
        from crypto_reviews.tasks import initialize_on_startup_check_update_crypto_review
        initialize_on_startup_check_update_crypto_review()
