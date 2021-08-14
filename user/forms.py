from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm



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
    
    six_digit_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'enter 6 digit code', 'maxlength':6,}))
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
                if query_email.authenticator_secret_code:      
                    if six_digit_code:
                        if pyotp.TOTP(str(query_email.authenticator_secret_code)).verify(str(six_digit_code)):
                            return six_digit_code             
                        else:
                            raise forms.ValidationError("The entered six digit code is wrong or you entered lesser than six digit")   
                    else:
                        raise forms.ValidationError("Your email is verified and you would got secret key.Enter 6 digit code")   
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