from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
import uuid

class CustomUser(AbstractUser):
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    authenticator_secret_code = models.CharField(max_length=500, blank=True)
    google_authenticator = models.BooleanField(default=False)
    authenticator_qrcode = models.ImageField(null=True, blank=True, upload_to='user_authenticator_qrcode_image')
    show_overall_login_history = models.BooleanField(default=True)
    show_last_modified_of_password = models.BooleanField(default=True)
    
    def get_obsolute_url(self):
        return reverse('dashboard', kwargs={
            'id': str(self.id)
        })

class PasswordChangeRequest(models.Model):
    user_email = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return f"{self.user_email}"