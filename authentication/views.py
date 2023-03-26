from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, 'authentication/index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
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
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save() # save to database after updating fields
        
        messages.success(request, "Your account has been successfully created")
        return redirect("signin")
    
    return render(request, 'authentication/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            fname = user.first_name
            print(fname)
            return render(request, 'authentication/index.html', {'fname': fname})
        else:
            messages.error(request, "Wrong username or password. Please try again")
            return redirect('home')
            
    return render(request, 'authentication/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out")
    return redirect('home')