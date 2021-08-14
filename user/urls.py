from allauth.account import views
from django.urls import path
from .views import *

urlpatterns = [
   
    path('passwords/change/', CustomPasswordChangeView.as_view(), name='account_change_password'),
    
    
    
]