from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import PasswordChangeRequest


CustomUser = get_user_model()
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',]
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'AUTHENTICATOR SECRET CODE',
            {
                'fields': 
                (
                    'authenticator_qrcode',
                    'authenticator_secret_code',
                    'google_authenticator',
                )
            }
        ),
        (
            'ACCOUNT SETTING',
            {
                'fields': 
                (
                    'show_overall_login_history',
                    'show_last_modified_of_password',
                )
            }
        )

    )
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PasswordChangeRequest)

