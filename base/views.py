from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def login_user(request):
    return render(request, 'login.html')
