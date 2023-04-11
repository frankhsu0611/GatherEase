from django.contrib.auth.models import User
from .models import UserProfile, Conference, Event
from datetime import datetime
import pytz

def get_events(request):    
    user = request.user
    if user.is_authenticated:
        local_timezone = pytz.timezone('America/Los_Angeles')
        now = datetime.now(local_timezone) #UTC time
        events_now = Event.objects.filter(conference = UserProfile.objects.get(user=user).conference,
                                    eventStartTime__lte = now,
                                    eventEndTime__gte = now,
                                    ).order_by('eventStartTime')
        events_following = Event.objects.filter(conference = UserProfile.objects.get(user=user).conference,
                                    eventStartTime__gte = now,
                                    ).order_by('eventStartTime')
        print(events_following)
        return (events_now, events_following)
    return None


    