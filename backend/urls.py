from django.contrib import admin
from django.urls import path, include
from appointments.views import homepage

urlpatterns = [
    path('', homepage),
    path('admin/', admin.site.urls),
    path('api/', include('appointments.urls')),
]
