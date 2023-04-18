from django.shortcuts import render
from django.db.models import Count
from authentication.models import Conference, UserProfile


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
