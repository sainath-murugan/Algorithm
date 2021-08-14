from allauth.account.signals import email_confirmed
from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
import pyotp

CustomUser = get_user_model()

@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):

    user = CustomUser.objects.get(email=email_address.email)
    secret_key = pyotp.random_base32()
    user.authenticator_secret_code = secret_key

    email = EmailMessage('it is your secret key',
    "we have provided you a secret key, don't share this key with anyone and download google authenticator and choose timebased authentication and use the otp every time to login.",
    f"Your secret code is = {secret_key}", 
    to=[email_address.email])

    email.send()

    user.save()

  
import platform
from algorithm_1.models import History

@receiver(user_logged_in)
def user_logged_in_(request, user, **kwargs):
    
    user = CustomUser.objects.get(email=user.email)
    try:
        system_os = platform.uname().system
    except:
        system_os = 'unknown'
    else:
        if system_os == 'Darwin':
            system_os = "MAC"
    try:
        system_name = platform.uname().node
    except:
        system_name = 'unknown'
    object = History.objects.create(user=user, system_os=str(system_os), system_name=str(system_name))
    object.save()