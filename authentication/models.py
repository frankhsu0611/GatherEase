from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


# Create your models here.
CONFERENCE_START_DATE = '2023-06-11'
CONFERENCE_END_DATE = '2023-06-16'
CONFERENCE_CODE = 'ICEASS2021'


class Conference(models.Model):
    conferenceCode = models.CharField(max_length=20, primary_key=True)
    conferenceName = models.CharField(
        max_length=100, default='adminConference')
    conferenceStartDate = models.DateField(default=CONFERENCE_START_DATE)
    conferenceEndDate = models.DateField(default=CONFERENCE_END_DATE)
    conferenceLocation = models.CharField(
        max_length=30, default='adminLocation')
    agenda = models.FileField(upload_to='agenda/')


class Track(models.Model):
    trackCode = models.CharField(max_length=20, primary_key=True)
    trackName = models.CharField(max_length=100)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    proceedings = models.FileField(upload_to='proceedings/')
    program = models.FileField(upload_to='program/')


class Ticket(models.Model):
    ticket_id = models.CharField(
        max_length=40, primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    checkin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.track.trackName}'

    def generate_ticket_id(self):
        return f"{self.user.pk}-{self.track.pk}-{uuid.uuid4()}"

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = self.generate_ticket_id()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('user', 'track')
        verbose_name_plural = "Tickets"


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
    paperTitle = models.CharField(max_length=200)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    userCategory = models.CharField(max_length=20)
    userCountry = models.CharField(max_length=20)
    userUniversity = models.CharField(max_length=40)
    tickets = models.ManyToManyField(Ticket)
    identifier = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "UserProfiles"

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(
                user=instance,
            )

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
