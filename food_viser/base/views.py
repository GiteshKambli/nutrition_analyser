from django.shortcuts import render
from .forms import UserImageForm
from .nutrition import get_nutrition
from .models import UploadImage
import numpy as np
import urllib.request
import cv2
import os
import matplotlib.pyplot as plt

from django.shortcuts import render
from django.http import JsonResponse
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
from tensorflow.python.keras.backend import set_session
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
# from tensorflow.keras.applications.imagenet_utils import decode_predictions
import matplotlib.pyplot as plt
import numpy as np
from keras.applications import vgg16
import datetime
import traceback


def home(request):
    return render(request, 'home.html')


def login_user(request):
    return render(request, 'login.html')


def scan_label(request):
    if request.method == 'POST':
        # form = UserImageForm(request.POST, request.FILES)
        # if form.is_valid():
        #     form.save()

        #     img_obj = form.instance
        #     img_url = img_obj.image.url
        #     print(img_url)
        #     img_url = r'{}'.format(img_url.replace('/', '\\'))
        #     print(img_url)
        #     new_path = 'food_viser' + img_url

        #     print(new_path)

        #     # print(type(img_url))
        #     # req = urllib.request.urlopen(img_url)
        #     # arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        #     img = cv2.imread(new_path)
        #     # print(type(img))
        #     # plt.imshow(img)
        #     # print(img.shape)
        #     # nutritions = get_nutrition(img)
        #     # print(nutritions)
        #     # , 'nutrition': nutritions
        #     return render(request, 'scan.html', {'form': form})
        f = request.FILES['sentFile']  # here you get the files needed
        response = {}
        file_name = "pic.jpg"
        file_name_2 = default_storage.save(file_name, f)
        file_url = default_storage.url(file_name_2).replace('/', '\\')
        print(file_url)
        original = load_img(file_url, target_size=(640, 640))
        numpy_image = img_to_array(original)

        nutritions = get_nutrition(numpy_image)
        print(nutritions)

        return render(request, 'scan.html')

    else:
        return render(request, 'scan.html')


# def search_recipe(request):
#     return render(request, 'search_recipe.html')
