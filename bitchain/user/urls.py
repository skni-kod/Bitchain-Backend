"""
URL mapping for user app.
"""
from django.urls import path, include

from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('me/image/', views.UpdateUserImageView.as_view(), name='me-image'),
    path('me/favorite-cryptocurrency/', views.FavoriteUserCryptocurrencyView.as_view(), name='me-favorite-cryptocurrency'),
    path('me/check-password/', views.CheckUserPasswordView.as_view(), name='me-check-password'),
    path('me/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    
]
