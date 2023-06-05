import io
import pytz
import base64
from django.contrib.auth.models import User
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect
from .models import UserProfile, Conference, Event, Paper, Track, Ticket
from datetime import datetime
from django.template.loader import get_template
from django.core.files.base import ContentFile
import qrcode
from io import BytesIO


def get_events(request):
    user = request.user
    if user.is_authenticated:
        local_timezone = pytz.timezone('America/Los_Angeles')
        now = datetime.now(local_timezone)  # UTC time
        events_now = Event.objects.filter(conference=UserProfile.objects.get(user=user).conference,
                                          eventStartTime__lte=now,
                                          eventEndTime__gte=now,
                                          ).order_by('eventStartTime')
        events_following = Event.objects.filter(conference=UserProfile.objects.get(user=user).conference,
                                                eventStartTime__gte=now,
                                                ).order_by('eventStartTime')
        print(events_following)
        return (events_now, events_following)
    return None


def get_tracks(request):
    user = request.user
    if user.is_authenticated:
        userProfile = UserProfile.objects.get(user=user)
        tracks = userProfile.tracks.all()
        return tracks
    return None

def download_proceedings(request, ticket_id):
    user = request.user
    if user.is_authenticated:
        ticket = Ticket.objects.get(ticket_id=ticket_id)
        track_code = ticket.track.trackCode
        track = Track.objects.get(trackCode=track_code)
        return FileResponse(track.proceedings, as_attachment=True)
    return redirect('sign-in')


def download_program(request, ticket_id):
    user = request.user
    if user.is_authenticated:
        ticket = Ticket.objects.get(ticket_id=ticket_id)
        track_code = ticket.track.trackCode
        track = Track.objects.get(trackCode=track_code)
        return FileResponse(track.program, as_attachment=True)
    return redirect('sign-in')

def download_certificate(request, ticket_id):
    user = request.user
    if user.is_authenticated:
        ticket = Ticket.objects.get(ticket_id=ticket_id)
        track_code = ticket.track.trackCode
        track = Track.objects.get(trackCode=track_code)
        return FileResponse(track.certificate, as_attachment=True)
    return redirect('sign-in')

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, "PNG")
    buffer.seek(0)
    img_data = buffer.getvalue()
    img_b64 = base64.b64encode(img_data).decode()
    return f'data:image/png;base64,{img_b64}'
    

# def dowload_certificate(request):
#     if request.user.is_authenticated:
#         paper = Paper.objects.get(user=request.user)
#         context = {
#             "user_profile": UserProfile.objects.get(user=request.user),
#             "paper": paper,
#             "background_image_data_uri": get_image_data_uri("static/img/certificate1.jpg"),
#         }
#         pdf = render_html_to_pdf('pages/certificate.html', context)

#         if pdf is None:
#             return HttpResponse("An error occurred while generating the PDF. Please check the server logs for more information.")

#         pdf_content = pdf.getvalue()
#         response = HttpResponse(pdf_content, content_type='application/pdf')
#         filename = "certificate.pdf"
#         response['Content-Disposition'] = f"attachment; filename={filename}"
#         return response
#     return redirect('sign-in')


# def render_html_to_pdf(template_src, context={}):
#     template = get_template(template_src)
#     html = template.render(context)
#     result = io.BytesIO()

#     HTML(string=html).write_pdf(result)

#     return result


# def get_image_data_uri(image_path):
#     with open(image_path, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#     return f"data:image/jpeg;base64,{encoded_string.decode('utf-8')}"


def merge_pdfs(pdfs):
    merged_pdf = pikepdf.Pdf.new()

    for pdf in pdfs:
        pdf_bytes = pdf.getvalue()
        src_pdf = pikepdf.Pdf.open(pdf_bytes)

        # Append all pages from the source PDF to the merged PDF
        for page in src_pdf.pages:
            merged_pdf.pages.append(page)

    merged_pdf_buffer = io.BytesIO()
    merged_pdf.save(merged_pdf_buffer)

    return merged_pdf_buffer
