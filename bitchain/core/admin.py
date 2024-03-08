from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core.models import (
    FavoriteUserCryptocurrency,
    UserFundTransaction, 
    UserFeatureTransaction,
    UserStackingTransaction,
    UserFundWallet,
    UserFeatureWallet,
    UserStackingWallet,
    User,
    UserWalletCryptocurrency,
    )
from crypto_reviews.models import CryptoReview


class UserAdmin(BaseUserAdmin):
    """User admin class"""
    ordering = ['id']
    list_display = ['email', 'full_name', 'nick_name', 'date_of_birth_format', 'pesel', 'account_balance', 'image']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'nick_name', 'date_of_birth', 'pesel', 'password1', 'password2', 'image'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('password', )}),
        (_('Personal info'), {'fields': ('full_name', 'nick_name', 'date_of_birth',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', )}),
    )
    readonly_fields = ('last_login',)

    def date_of_birth_format(self, obj):
        return obj.date_of_birth.strftime("%Y-%m-%d")
    date_of_birth_format.short_description = 'Date of birth'




class FavoriteUserCryptocurrencyAdmin(admin.ModelAdmin):
    """FavoriteUserCryptocurrency admin class"""
    list_display = ['user', 'favorite_crypto_symbol']
    

admin.site.register(User, UserAdmin)
admin.site.register(FavoriteUserCryptocurrency, FavoriteUserCryptocurrencyAdmin)
admin.site.register(CryptoReview)
admin.site.register(UserFundTransaction) 
admin.site.register(UserFeatureTransaction)
admin.site.register(UserStackingTransaction)
admin.site.register(UserFundWallet)
admin.site.register(UserFeatureWallet)
admin.site.register(UserStackingWallet)