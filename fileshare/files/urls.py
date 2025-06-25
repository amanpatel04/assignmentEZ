from django.urls import path
from . import views


urlpatterns = [
  path('', views.get_file, name='get_file'),
  path('upload/', views.upload_file, name='upload_file'),
]