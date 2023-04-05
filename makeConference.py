import os
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gte.settings')
django.setup()


from django.utils import timezone
from authentication.models import Conference

# Define the conference details
conference_code = 'ICEASS2021'
conference_name = 'adminConference'
conference_start_date = timezone.datetime(2023, 6, 11).date()
conference_end_date = timezone.datetime(2023, 6, 16).date()
conference_type = 'adminConferenceType'
conference_location = 'adminConferenceLocation'

# Create a new Conference instance
conference = Conference(
    conferenceCode=conference_code,
    conferenceName=conference_name,
    conferenceStartDate=conference_start_date,
    conferenceEndDate=conference_end_date,
    conferenceLocation=conference_location,
    conferenceType=conference_type,
)

# Save the Conference instance to the database
conference.save()
