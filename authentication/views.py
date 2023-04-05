from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile, Conference

# Create your views here.
def home(request):
    user = request.user
    if user.is_authenticated:
        userProfile = UserProfile.objects.get(user=user)
        conference = userProfile.conference
        context = {'userProfile': userProfile, 'conference': conference}
        return render(request, 'authentication/index1.html', context)
    return render(request, 'authentication/index.html')

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
        
        if userCategory not in ['speaker', 'attendee']: # add more user categories here
            messages.error(request, "User category must be speaker or attendee")
            return redirect('home')
        
        if conferenceCode not in ['ICEASS2021', 'ICEASS2022', 'ICEASS2023']: # add more conference codes here
            messages.error(request, "Conference code is invalid")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save() # save to database after updating fields
        update_user_profile(request, myuser)
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
            #return render(request, 'authentication/index.html', {'fname': fname})
            return redirect('home')
        else:
            messages.error(request, "Wrong username or password. Please try again")
            logout(request) # logout user if they are already logged in
            return redirect('sign-in')
            
    return render(request, 'authentication/sign-in.html')

def signout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out")
    return redirect('home')

def update_user_profile(request, user):
    user.userprofile.userCategory = request.POST['userCategory']
    user.userprofile.conferenceCode = Conference.objects.get(conferenceCode = request.POST['conferenceCode'])
    user.userprofile.userCountry = request.POST['userCountry']
    user.save()

def agenda(request):
    return render(request, 'pages/agenda.html')

def download(request):
    return render(request, 'pages/download.html')