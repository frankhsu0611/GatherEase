from django.shortcuts import redirect, render
from django.db.models import Count
import openpyxl
from authentication.models import Conference, UserProfile, Event
from .forms import AdminEventFileUploadForm




def home_dashboard(request):
    conferences = Conference.objects.all()

    # Prepare data for chart
    chart_data = []
    for conference in conferences:
        user_profiles = UserProfile.objects.filter(conference=conference)
        country_count = user_profiles.values(
            'userCountry').annotate(count=Count('userCountry'))
        chart_data.append({
            'conference': conference.conferenceName,
            'country_count': list(country_count),
        })

    return render(request, 'custom_admin_dashboard/home_dashboard.html', {
        'chart_data': chart_data,
    })
    
# custom_admin_dashboard/admin.py

def upload_event_file(request):
    if request.method == 'POST':
        form = AdminEventFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            event_file = request.FILES['event_file']
            wb = openpyxl.load_workbook(event_file)
            sheet = wb.active
            for row in sheet.iter_rows(min_row=2):  # Skip header row
                event = Event(
                    eventCode=row[0].value,
                    eventTheme=row[1].value,
                    eventStartTime=row[2].value,
                    eventEndTime=row[3].value,
                    conference_id=row[4].value,  # Assuming conference_id is stored in the Excel file
                    keynoteSpeaker=row[5].value,
                    eventRoom=row[6].value,
                )
                event.save()
            # Redirect to the Event list page in the admin site
            return redirect('admin:authentication_event_changelist')
    else:
        form = AdminEventFileUploadForm()
    return render(request, 'admin/upload_event_file.html', {'form': form})


