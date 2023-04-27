from django.shortcuts import redirect, render
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib import messages
import openpyxl
from authentication.models import Conference, UserProfile, Event, Paper
from .forms import AdminEventFileUploadForm, AdminUserProfileFileUploadForm, AdminPaperFileUploadForm




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


def upload_userprofiles_file(request):
    if request.method == 'POST':
        form = AdminUserProfileFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user_profiles_file = request.FILES['user_profiles_file']
            wb = openpyxl.load_workbook(user_profiles_file)
            sheet = wb.active
            for row in sheet.iter_rows(min_row=2):  # Skip header row
                username = row[0].value
                fname = row[1].value
                lname = row[2].value
                email = row[3].value
                password = row[4].value
                user_category = row[5].value
                user_country = row[6].value
                conferenceCode = row[7].value  # Assuming conferenceCode is stored in the Excel file
                user_univeristy = row[8].value

                user, created = User.objects.get_or_create(
                    username=username,
                    email=email,
                )
                if created:
                    user.set_password(password)
                    user.first_name = fname
                    user.last_name = lname
                    user.save()

                user.userprofile.userCategory = user_category
                user.userprofile.userCountry = user_country
                user.userprofile.conference = Conference.objects.get(conferenceCode=conferenceCode)
                user.userprofile.userUniversity = user_univeristy
                user.save() # Save the both user and UserProfile model instance 
            messages.success(request, "User profiles have been successfully imported.")
            
            #URL pattern of admin follows the singular form of the model name
            return redirect('admin:authentication_userprofile_changelist') 
    else:
        form = AdminUserProfileFileUploadForm()

    return render(request, 'admin/upload_userprofiles_file.html', {'form': form})

def upload_paper_file(request):
    if request.method == 'POST':
        form = AdminPaperFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            paper_file = request.FILES['paper_file']
            wb = openpyxl.load_workbook(paper_file)
            sheet = wb.active
            for row in sheet.iter_rows(min_row=2):  # Skip header row
                user_email = row[0].value
                user = User.objects.get(email=user_email)
                paper = Paper(
                    user=user,
                    paperID=row[1].value,
                    paperTitle=row[2].value,
                )
                paper.save()
            return redirect('admin:authentication_paper_changelist')
    else:
        form = AdminPaperFileUploadForm()
    return render(request, 'admin/upload_paper_file.html', {'form': form})