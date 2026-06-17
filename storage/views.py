from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import UploadedFile


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        UploadedFile.objects.create(
            user=request.user,
            file=request.FILES['file']
        )

    files = UploadedFile.objects.filter(user=request.user)

    return render(request, 'dashboard.html', {'files': files})