from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("login/", views.login_user, name='login'),
    path('scan/', views.scan_label, name="scan"),
]
