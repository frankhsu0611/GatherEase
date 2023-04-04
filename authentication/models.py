from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

CONFERENCE_START_DATE = '%2023-%6-%11'
CONFERENCE_END_DATE = '2023-%6-%16'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    userCategory = models.CharField(max_length=20)
    conferenceCode = models.CharField(max_length=20)
    userCountry = models.CharField(max_length=20)
    ConferenceStartDate = models.DateField(default=CONFERENCE_START_DATE)
    ConferenceEndDate = models.DateField(default=CONFERENCE_END_DATE)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()