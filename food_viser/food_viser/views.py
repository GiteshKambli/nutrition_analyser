from .nutrition import get_nutrition
from django.shortcuts import render
from django.core.files.storage import default_storage
import cv2


def home(request):
    return render(request, 'home.html')


def scan_label(request):
    if request.method == 'POST':
        f = request.FILES['sentFile']  # here you get the files needed
        response = {}
        file_name = "pic.jpg"
        file_name_2 = default_storage.save(file_name, f)
        file_url = r'../food_viser/' + default_storage.url(file_name_2)
        print(file_url)
        img = cv2.imread(file_url)
        nutrition = get_nutrition(img, ocr='easyocr')
        print(nutrition)

        return render(request, 'scan.html', {'nutrition': nutrition[0]})

    return render(request, 'scan.html')
