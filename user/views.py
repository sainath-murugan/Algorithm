from django.shortcuts import render, redirect
from allauth.account.views import PasswordChangeView, SignupView
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .forms import TwoMFA, CustomPasswordResetForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


CustomUser = get_user_model()

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView): #allauth
    success_url = '/'


class CustomSignupView(SignupView):

    def form_valid(self, form):
        self.user = form.save(self.request)
        return redirect('account_login')

@login_required(login_url='account_login')
def two_factor_authentication(request, id):
    
    current_user = get_object_or_404(CustomUser, id=id)
    if current_user != request.user:                   
        return HttpResponseBadRequest('error 404')
    else:
        form = TwoMFA(request=request) #request=request is due to TwoMFA form class
        if request.method == 'POST':
            form = TwoMFA(request.POST, request=request) #request=request is due to TwoMFA form class
            if form.is_valid():
                return redirect('settings',id=str(request.user.id))
            
    context = {
        'form':form
    }
    return render(request, 'two_factor_authentication.html', context)

def custom_password_reset(request):

    form = CustomPasswordResetForm(request=request) ##request=request is due to CustomPasswordResetForm form class
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST, request=request) ##request=request is due to CustomPasswordResetForm form class
        if form.is_valid():
            form.save()
            messages.success(request, f"your email has sent to Algorithm please wait for respond it takes some time")
            return redirect('custom_password_reset')
    context = {
        'form':form
    }
    return render(request, 'account/custom_password_reset.html', context)