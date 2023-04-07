import os
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gte.settings')
django.setup()


from django.utils import timezone
from authentication.models import Event
from authentication.models import Conference
from datetime import datetime
from dateutil import tz
import pytz

eventCode = "EVENT101"
eventTheme = 'adminEventTheme'
conference = Conference.objects.get(conferenceCode = 'ICEASS2021')
keynoteSpeaker = "adminKeynoteSpeaker"
eventRoom = "adminEventRoom"
eventStartTime = datetime(2023, 4, 4, 15, 0)
eventEndTime = datetime(2023, 4, 20, 20, 0)

event = Event(eventCode = eventCode, 
              eventTheme = eventTheme, 
              eventStartTime = eventStartTime,
              eventEndTime = eventEndTime,
              conference = conference, 
              keynoteSpeaker = keynoteSpeaker, 
              eventRoom = eventRoom,
              )

event.save()
    