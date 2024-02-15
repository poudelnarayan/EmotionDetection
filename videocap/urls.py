# In <app_name>/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.take_photo, name='videocapture'),
    path('view_emotion/<str:detected_emotion>/',
         views.view_emotion, name='view_emotion'),
    # Add more URL patterns as needed
]
