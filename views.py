from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
#from django.http import HttpResponse
from .forms import RegisterForm
from .forms import VideoUploadForm
from .accident_detection import process_video
import os

def home(request):
    accident_report = None
    report_path = "Accident.txt"

    if os.path.exists(report_path):
        with open(report_path, "r") as file:
            accident_report = file.read()
    
    return render(request, 'tracking/home.html', {"accident_report": accident_report})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  
            user.save()
            login(request, user)  
            return redirect('upload_video')  
    else:
        form = RegisterForm()
    
    return render(request, 'tracking/register.html', {'form': form})


def login_view(request):
    error = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('upload_video')  
            else:
                error = "Invalid username or password"
    else:
        form = LoginForm()
    
    return render(request, 'tracking/login.html', {'form': form, 'error': error})


def upload_and_detect(request):
    result = None  
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES["video"]
            video_path = f"media/videos/{video_file.name}"

            
            with open(video_path, "wb+") as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)


            result = process_video(video_path)

    else:
        form = VideoUploadForm()

    return render(request, "tracking/upload_detect.html", {"form": form, "result": result})
    