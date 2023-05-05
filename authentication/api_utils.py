import io
from django.contrib.auth.models import User
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect
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


def download_proceedings(request):
    user = request.user
    if user.is_authenticated:
        userProfile = UserProfile.objects.get(user=user)
        conference = userProfile.conference
        proceedings = conference.proceedings
        return FileResponse(proceedings, as_attachment=True)
    return redirect('sign-in')

def download_program(request):
    user = request.user
    if user.is_authenticated:
        userProfile = UserProfile.objects.get(user=user)
        conference = userProfile.conference
        program = conference.program
        return FileResponse(program, as_attachment=True)
    


from xhtml2pdf import pisa
from django.template.loader import get_template



def dowload_certificate(request):
    context = {
        "userProfile": UserProfile.objects.get(user=request.user),
    }

    pdf = render_to_pdf('pages/certificate.html', context)

    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" %("12341231")
        content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")



def render_to_pdf(template_src, context={}):
    template = get_template(template_src)
    html = template.render(context)
    result = io.BytesIO()

    info = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)

    if not info.err:
        return FileResponse(result.getvalue(), content_type='application/pdf')

    return None


