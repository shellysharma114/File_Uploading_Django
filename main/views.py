from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import FileUpload
from django.contrib import messages

def home(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You have to login first to access the home page.')
        return redirect('signin')
    else:
        all_files = FileUpload.objects.filter(user=request.user)
        params = {'files': all_files}
        return render(request, 'home.html', params)

def signup(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        username_exists = User.objects.filter(username=username)
        email_exists = User.objects.filter(email=email)

        if(username_exists or email_exists):
            messages.error(request, 'Username or email is already exists.')
        else:
            new_user = User.objects.create_user(username=username, email=email, password=password)
            new_user.save()
            return redirect('signin')
    return render(request, 'signup.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'signin.html')

def signout(request):
    logout(request)
    return redirect('signin')

def fileUpload(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            file_name = request.FILES.get('file_name')
            if(file_name):
                upload_file = FileUpload.objects.create(user=request.user, file=file_name)
                upload_file.save()
            return redirect('home')
        else:
            return HttpResponse("Not loggedin")
    return HttpResponse("fileupload")