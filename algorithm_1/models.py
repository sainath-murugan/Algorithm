from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
import uuid

class Vault(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='profile_user', on_delete=models.CASCADE)
    key = models.CharField(max_length=50, blank=False)
    value = models.CharField(max_length=500, blank=False)
    last_modified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} | Vault"
    
    def get_obsolute_url_for_edit(self):
        return reverse('edit_password', kwargs={
            'id': str(self.id)
        })

    def get_obsolute_url_for_delete(self):
        return reverse('delete_password', kwargs={
            'id': str(self.id)
        })
    
    def get_obsolute_url_for_view(self):
        return reverse('view_password', kwargs={
            'id': str(self.id)
        })

class History(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='profile_user_history', on_delete=models.CASCADE)
    logged_in_at = models.DateTimeField(default=timezone.now)
    system_os = models.CharField(max_length=50, blank=True)
    system_name = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.username} | History"

    def get_obsolute_url_setting(self):
        return reverse('settings', kwargs={
            'id': str(self.id)
        })

class FeedBack(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='profile_user_feedback', on_delete=models.SET_NULL, null=True)
    feedback = models.TextField()

    def __str__(self):
        return f"feedback"


