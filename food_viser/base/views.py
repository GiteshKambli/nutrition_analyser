from django.shortcuts import render
from .forms import UserImageForm
from .models import UploadImage


def home(request):
    return render(request, 'home.html')


def login_user(request):
    return render(request, 'login.html')


def scan_label(request):
    if request.method == 'POST':
        form = UserImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            # Getting the current instance object to display in the template
            img_object = form.instance

            return render(request, 'scan.html', {'form': form, 'img_obj': img_object})
    else:
        form = UserImageForm()

    return render(request, 'scan.html', {'form': form})
