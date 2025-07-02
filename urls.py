from django.urls import path
from . import views

urlpatterns = [
    path('', views.uploadHomePage, name='upload'),
    path('uploadFormSubmit', views.uploadFormSubmit, name='uploadFormSubmit'),
    path('generatePresignedURL', views.generate_presigned_url, name='generatePresignedURL'),
]
