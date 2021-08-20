from allauth.account import views
from django.urls import path
from .views import *

urlpatterns = [
   
    path('passwords/change/', CustomPasswordChangeView.as_view(), name='account_change_password'),
    path('signUp/', CustomSignupView.as_view(), name="account_signup"),
    path('two_factor_authentication/<uuid:id>/', two_factor_authentication, name='two_factor_authentication'),
    path('custom_password_reset/', custom_password_reset, name='custom_password_reset'),
    
    
    
]