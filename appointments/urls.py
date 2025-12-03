from django.urls import path
from . import views

urlpatterns = [
    path('hospitals/', views.list_hospitals, name='hospitals'),
    path('doctors/<int:hospital_id>/', views.list_doctors, name='doctors'),
    path('book/', views.book_appointment, name='book'),
]
