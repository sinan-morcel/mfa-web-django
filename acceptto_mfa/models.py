from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class AccepttoCredentials(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  mfa_email = models.EmailField(blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        AccepttoCredentials.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.accepttocredentials.save()


