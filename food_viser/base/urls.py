from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name='home'),
    path("login/", views.login_user, name='login'),
    path('scan/', views.scan_label, name="scan"),
    # path('search-recipe/', views.search_recipe, name='search-recipe'),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
