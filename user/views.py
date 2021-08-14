from django.shortcuts import render, redirect
from allauth.account.views import PasswordChangeView, EmailView
from django.http import HttpResponseBadRequest
# Create your views here.


class CustomPasswordChangeView(PasswordChangeView): #allauth
    success_url = '/'

