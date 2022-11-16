from django.shortcuts import render
from .forms import UserImageForm
from .nutrition import get_nutrition
from .models import UploadImage
import numpy as np
import cv2.cv2 as cv2


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
            print(img_object)
            # img = cv2.imread(img_object)
            # img_object = cv2.cvtColor(numpy.array(img_object), cv2.COLOR_RGB2BGR)
            # nutritions = get_nutrition(img_object) #, 'nutrition': img

            return render(request, 'scan.html', {'form': form})
    else:
        form = UserImageForm()

    return render(request, 'scan.html', {'form': form})


# def search_recipe(request):
#     return render(request, 'search_recipe.html')
