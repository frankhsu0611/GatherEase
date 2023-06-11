from django.shortcuts import redirect, render
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile, Conference, Event, Paper, Track, Ticket
from django.shortcuts import get_object_or_404
from .api_utils import generate_qr_code, get_events

# Create your views here.


def home(request):
    user = request.user
    if user.is_authenticated:
        tickets = Ticket.objects.filter(user=user)
        context = {"tickets": tickets}
        return render(request, 'authentication/index.html', context)
    return render(request, 'authentication/index.html')


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
        userProfile = UserProfile.objects.get(user=user)
        track = ticket.track
        conference = track.conference
        ticket = get_object_or_404(Ticket, user=user, track=track)
        qr_code = generate_qr_code(str(ticket_id))
        events_now, events_following = get_events(request, conference)
        context = {
            "ticket": ticket,
            "userProfile": userProfile,
            "track": track,
            "conference": conference,
            "qr_code": qr_code,
            "events_now": events_now,
            "events_following": events_following,
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


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to keep the user logged in
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was changed successfully!')
            return redirect('password_change_done')
        else:
            old_password_errors = form.errors.get('old_password')
            new_password_errors = form.errors.get('new_password2')

            if old_password_errors:
                messages.error(
                    request, 'Invalid old password. Please try again.')

            if new_password_errors:
                messages.error(
                    request, 'Invalid new password. Please ensure your password meets the requirements.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'authentication/password_change.html', {'form': form})


@login_required
def password_change_done(request):
    return render(request, 'authentication/password_change_done.html')


def about_us(request):
    return render(request, 'pages/about_us.html')


def signout(request):
    logout(request)
    # messages.success(request, "You have been successfully logged out")
    return redirect('home')

# write a function to show agenda page and pass a http response that contains the agenda.pdf stored in media/ducoment folder


def agenda(request, ticket_id):
    user = request.user
    if user.is_authenticated:
        ticket = Ticket.objects.get(ticket_id=ticket_id)
        track_code = ticket.track.trackCode
        track = get_object_or_404(Track, trackCode=track_code)
        conference = track.Conference
        context = {"ticket": ticket, "track": track, "conference": conference}
        return render(request, 'pages/agenda.html', context)
    return redirect('sign-in')


def download(request, ticket_id):
    user = request.user
    if user.is_authenticated:
        ticket = Ticket.objects.get(ticket_id=ticket_id)
        track_code = ticket.track.trackCode
        track = get_object_or_404(Track, trackCode=track_code)
        conference = track.Conference
        context = {"ticket": ticket, "track": track, "conference": conference}
        return render(request, 'pages/download.html', context)
    return redirect('sign-in')


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
