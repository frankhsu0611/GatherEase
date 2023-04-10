import os
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gte.settings')
django.setup()


from django.utils import timezone
from authentication.models import Event
from authentication.models import Conference
from datetime import datetime
import pytz

eventCode = "EVENT102"
eventTheme = 'adminEventTheme'
conference = Conference.objects.get(conferenceCode = 'ICEASS2021')
keynoteSpeaker = "adminKeynoteSpeaker"
eventRoom = "adminEventRoom"

# choose local timezone to deploy
local_timezone = pytz.timezone('America/Los_Angeles')
eventStartTime = timezone.datetime(2023, 4, 15, 16, 12, 30, tzinfo=local_timezone)
eventEndTime = timezone.datetime(2023, 4, 20, 20, 18, 30, tzinfo=local_timezone)


event = Event(eventCode = eventCode, 
              eventTheme = eventTheme, 
              eventStartTime = eventStartTime,
              eventEndTime = eventEndTime,
              conference = conference, 
              keynoteSpeaker = keynoteSpeaker, 
              eventRoom = eventRoom,
              )

event.save()
    