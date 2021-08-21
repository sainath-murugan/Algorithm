from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
import uuid


class UserQrcode(models.Model):

    authenticator_qrcode = models.ImageField(null=True, blank=True, upload_to='user_authenticator_qrcode_image')
    authenticator_secret_code = models.CharField(max_length=500, blank=True)
    
    def __str__(self):
        return f"{self.authenticator_qrcode} | {self.authenticator_secret_code}"

class CustomUser(AbstractUser):
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    authenticator_secret_code = models.CharField(max_length=500, blank=True)
    google_authenticator = models.BooleanField(default=False)
    show_overall_login_history = models.BooleanField(default=True)
    show_last_modified_of_password = models.BooleanField(default=True)
    qr_code = models.ForeignKey(UserQrcode, related_name='profile_user_qrcode', on_delete=models.SET_NULL, null=True, blank=True)
    
    def get_obsolute_url(self):
        return reverse('dashboard', kwargs={
            'id': str(self.id)
        })


class PasswordChangeRequest(models.Model):
    user_email = models.CharField(max_length=150, blank=False)
    requested_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user_email}"