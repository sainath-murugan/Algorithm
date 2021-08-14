from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import Vault
from django.utils import timezone

@receiver(pre_save, sender=Vault)
def last_modified(sender, instance, *args, **kwargs):
    instance.last_modified =  timezone.now()