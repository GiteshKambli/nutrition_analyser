from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    # path('', include('base.urls')),
    path("", views.home, name='home'),
    path('scan/', views.scan_label, name="scan"),
]


