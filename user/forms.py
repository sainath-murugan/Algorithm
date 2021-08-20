from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import PasswordChangeRequest



class CustomUserCreationForm(UserCreationForm):
    class Meta:
       model = get_user_model()
       fields =  ('email', 'username',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)


# allauth
#login
from django import forms
from allauth.account.forms import LoginForm
from django.contrib.auth import get_user_model
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth import authenticate
import pyotp


CustomUser = get_user_model()

class MyCustomLoginForm(LoginForm):
    
    six_digit_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'enter 6 digit code (if 2FA Enabled)', 'maxlength':6,}))
    six_digit_code.required = False
    six_digit_code.label = False

    def clean_six_digit_code(self):

        user_email = self.cleaned_data['login']
        user_password = self.cleaned_data['password']
        six_digit_code = self.cleaned_data['six_digit_code']
        try:
            query_email = CustomUser.objects.get(email=user_email) 
        except:
            pass   
        else:
            if authenticate(email=user_email, password=user_password): 
                query_email = CustomUser.objects.get(email=user_email) 
                if query_email.google_authenticator:      
                    if six_digit_code:
                        if pyotp.TOTP(str(query_email.authenticator_secret_code)).verify(str(six_digit_code)):
                            return six_digit_code             
                        else:
                            raise forms.ValidationError("The entered six digit code is wrong or you entered lesser than six digit")   
                    else:
                        raise forms.ValidationError("You have enabled Two factor authentication, you must enter the 6 digit code")   
                else:
                    pass
            else:
                pass
                              
    def login(self, *args, **kwargs):
        
        return super(MyCustomLoginForm, self).login(*args, **kwargs)
 
class AccountSettings(ModelForm):

    class Meta:

       model = get_user_model()
       fields =  ('show_overall_login_history','show_last_modified_of_password')

class DeleteAccount(forms.Form):

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop("request")
        super(DeleteAccount, self).__init__(*args, **kwargs)

    email = forms.EmailField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'email'}))
    password = forms.CharField(max_length=150, widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    six_digit_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'enter 6 digit code', 'maxlength':6,}), help_text='enter six digit code after verifing captcha')
    six_digit_code.required = True
    six_digit_code.label = False
    recaptcha = ReCaptchaField(widget = ReCaptchaV2Checkbox(attrs={    
              'data-size': 'compact',
          }))
   
    def clean_email(self):

        user_email = self.cleaned_data['email']
        if self.request.user.email == user_email:
            return user_email
        else:
            raise forms.ValidationError("Entery your correct email")   


    def clean_password(self):

        user_password = self.cleaned_data['password']
        if authenticate(email=self.request.user.email, password=user_password):
                return user_password 
        else:
            raise forms.ValidationError("Enter your correct password")   
        

    def clean_six_digit_code(self):

        six_digit_code = self.cleaned_data['six_digit_code']
        if pyotp.TOTP(str(self.request.user.authenticator_secret_code)).verify(str(six_digit_code)):
            return six_digit_code
        else:
            raise forms.ValidationError("Enter your correct six digit code") 

class TwoMFA(forms.Form):

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop("request")
        super(TwoMFA, self).__init__(*args, **kwargs)

    six_digit_code = forms.CharField(max_length=6, label=False, widget=forms.TextInput(attrs={'placeholder': 'enter 6 digit code', 'maxlength':6,}))

    def clean_six_digit_code(self):

        six_digit_code = self.cleaned_data['six_digit_code']
        if pyotp.TOTP(str(self.request.user.authenticator_secret_code)).verify(str(six_digit_code)):
            if self.request.user.google_authenticator:
                self.request.user.google_authenticator = False
                self.request.user.save()
            else:
                self.request.user.google_authenticator = True
                self.request.user.save()
            return six_digit_code
        else:
            raise forms.ValidationError("Enter the correct six digit code") 


class CustomPasswordResetForm(ModelForm):
    
    class Meta:
        model = PasswordChangeRequest
        fields = [
            'user_email',
        ]
        widgets = {
            'user_email': forms.TextInput(attrs={'placeholder': 'enter your email'}),
        }

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop("request")
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)

    def clean_user_email(self):

        user_email = self.cleaned_data['user_email']
        if self.request.user.is_authenticated:
            if self.request.user.email == user_email:
                return user_email
            else:
                raise forms.ValidationError("Enter your correct email")  
        else:
            try:
                query_email = CustomUser.objects.get(email=user_email) 
            except:
                raise forms.ValidationError("No user with this address")   
            else:
                return user_email
         