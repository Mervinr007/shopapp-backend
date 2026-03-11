from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from myapp.views_auth import google_callback_complete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapp.urls')),
    path('accounts/', include('allauth.urls')),
    path('oauth/complete/', google_callback_complete),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)