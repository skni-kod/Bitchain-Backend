from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CryptoReview
from .serializers import CryptoReviewSerializer
from django.utils import timezone

from drf_spectacular.utils import extend_schema


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CryptoReview
from .serializers import CryptoReviewSerializer
from django.utils import timezone

from drf_spectacular.utils import extend_schema

def get_or_create_crypto_review(symbol):
    try:
        crypto_review = CryptoReview.objects.get(symbol=symbol)
    except CryptoReview.DoesNotExist:
        if len(symbol) > 10:
            raise ValueError("Symbol too long. Maximum length is 10.")
        crypto_review = CryptoReview.objects.create(symbol=symbol)
        crypto_review.last_reset_date = timezone.now().date()
        crypto_review.save()
    return crypto_review

@extend_schema(
    description="Get or create a CryptoReview for the specified symbol.",
    responses={status.HTTP_200_OK: CryptoReviewSerializer}
)
class CryptoReviewView(APIView):

    def get(self, request, symbol):
        crypto_review = get_or_create_crypto_review(symbol)
        serializer = CryptoReviewSerializer(crypto_review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request={
            "application/json": {
                "example": {"action": "good"},
            }
        },
        responses={200: CryptoReviewSerializer(many=False),
                   400: {"error": "Action not provided"},
                   404: {"error": "CryptoReview not found for symbol"}
        },
        description="If action is 'good' or 'bad', increment the count for the specified symbol."
    )
    def patch(self, request, symbol):
        crypto_review = get_or_create_crypto_review(symbol)

        action = request.data.get('action', None)
        if action:
            if action == 'good':
                crypto_review.good += 1
            elif action == 'bad':
                crypto_review.bad += 1

            crypto_review.save()
            serializer = CryptoReviewSerializer(crypto_review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Action not provided"}, status=status.HTTP_400_BAD_REQUEST)
