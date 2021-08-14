from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


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
                    'authenticator_secret_code',
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

