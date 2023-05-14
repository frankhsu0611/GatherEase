from django.shortcuts import redirect, render
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile, Conference, Event, Paper, Track, Ticket
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

# Create your views here.


def home(request):
    user = request.user
    if user.is_authenticated:
        tickets = Ticket.objects.filter(user=user)
        context = {"tickets": tickets}
        return render(request, 'authentication/index.html', context)
    return render(request, 'authentication/index1.html')


# def ticket(request, track_code):
#     user = request.user
#     if user.is_authenticated:
#         userProfile = UserProfile.objects.get(user=user)
#         track = get_object_or_404(Track, trackCode=track_code)
#         conference = track.Conference
#         context = {"userProfile": userProfile,
#                    "track": track, "conference": conference}
#         return render(request, 'authentication/ticket.html', context)
#     return render(request, 'authentication/index1.html')

def ticket(request, ticket_id):
    user = request.user
    if user.is_authenticated:
        ticket = Ticket.objects.get(ticket_id=ticket_id)
        track_code = ticket.trackCode
        userProfile = UserProfile.objects.get(user=user)
        track = get_object_or_404(Track, trackCode=track_code)
        conference = track.Conference
        ticket = get_object_or_404(Ticket, user=user, trackCode=track_code)
        qr_code = generate_qr_code(str(ticket.id))
        context = {
            "ticket": ticket,
            "userProfile": userProfile,
            "track": track,
            "conference": conference,
            "qr_code": qr_code
        }
        return render(request, 'authentication/ticket.html', context)
    return render(request, 'authentication/index1.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        userCategory = request.POST['userCategory']
        userCountry = request.POST['userCountry']
        userUniversity = request.POST['userUniversity']
        conferenceCode = request.POST['conferenceCode']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('home')

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric")
            return redirect('home')

        # add more user categories here
        if userCategory not in ['speaker', 'attendee']:
            messages.error(
                request, "User category must be speaker or attendee")
            return redirect('home')

        # add more conference codes here
        if conferenceCode not in ['ICEASS2021', 'ICEASS2022', 'ICEASS2023']:
            messages.error(request, "Conference code is invalid")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.userprofile.userCategory = userCategory
        myuser.userprofile.conference = Conference.objects.get(
            conferenceCode=request.POST['conferenceCode'])
        myuser.userprofile.userCountry = userCountry
        myuser.userprofile.userUniversity = userUniversity
        myuser.save()
        messages.success(request, "Your account has been successfully created")
        return redirect("sign-in")

    return render(request, 'authentication/sign-up.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            fname = user.first_name
            # return render(request, 'authentication/index.html', {'fname': fname})
            return redirect('home')
        else:
            messages.error(
                request, "Wrong username or password. Please try again")
            logout(request)  # logout user if they are already logged in
            return redirect('sign-in')

    return render(request, 'authentication/sign-in.html')


def signout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out")
    return redirect('home')

# write a function to show agenda page and pass a http response that contains the agenda.pdf stored in media/ducoment folder


def agenda(request, ticket_id):
    user = request.user
    if user.is_authenticated:
        ticket = Ticket.objects.get(ticket_id=ticket_id)
        track_code = ticket.trackCode
        track = get_object_or_404(Track, trackCode=track_code)
        conference = track.Conference
        context = {"ticket": ticket, "track": track, "conference": conference}
        return render(request, 'pages/agenda.html', context)
    return redirect('sign-in')


def download(request, ticket_id):
    user = request.user
    if user.is_authenticated:
        ticket = Ticket.objects.get(ticket_id=ticket_id)
        track_code = ticket.trackCode
        track = get_object_or_404(Track, trackCode=track_code)
        conference = track.Conference
        context = {"ticket": ticket, "track": track, "conference": conference}
        return render(request, 'pages/download.html', context)
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
    return ContentFile(buffer.read(), 'qr_code.png')


# def certificate(request):
#     if request.user.is_authenticated:
#         user = request.user
#         user_profile = UserProfile.objects.get(user=user)
#         paper = Paper.objects.get(user=user)

#         context = {
#             'user_profile': user_profile,
#             'paper': paper,
#             #"background_image_data_uri": get_image_data_uri("static/img/certificate1.jpg"),
#         }

#         return render(request, 'pages/certificate.html', context)
#     else:
#         messages.error(request, "Please log in to view your certificate.")
#         return redirect('sign-in')
