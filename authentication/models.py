from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
CONFERENCE_START_DATE = '2023-06-11'
CONFERENCE_END_DATE = '2023-06-16'
CONFERENCE_CODE = 'ICEASS2021'


class Conference(models.Model):
    conferenceCode = models.CharField(max_length=20, primary_key=True)
    conferenceName = models.CharField(max_length=20, default='adminConference')
    conferenceStartDate = models.DateField(default=CONFERENCE_START_DATE)
    conferenceEndDate = models.DateField(default=CONFERENCE_END_DATE)
    conferenceLocation = models.CharField(
        max_length=30, default='adminLocation')
    conferenceType = models.CharField(max_length=20, default='adminType')
    # Specify the sub-directory within 'media' folder.
    agenda = models.FileField(upload_to='agenda/')
    # Specify the sub-directory within 'media' folder.
    proceedings = models.FileField(upload_to='proceedings/')
    #TO DO: add program


class Event(models.Model):
    eventCode = models.CharField(max_length=20, primary_key=True)
    eventTheme = models.CharField(max_length=20)
    eventStartTime = models.DateTimeField()
    eventEndTime = models.DateTimeField()
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    keynoteSpeaker = models.CharField(max_length=20)
    eventRoom = models.CharField(max_length=20)

class Paper(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paperID = models.CharField(max_length=20, primary_key=True)
    paperTitle = models.CharField(max_length=50)

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    userCategory = models.CharField(max_length=20)
    userCountry = models.CharField(max_length=20)
    userUniversity = models.CharField(max_length=40)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    
    
    class Meta:
        verbose_name_plural = "UserProfiles"

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(
                user=instance,
                conference=Conference.objects.get(
                    conferenceCode=CONFERENCE_CODE),
            )

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
