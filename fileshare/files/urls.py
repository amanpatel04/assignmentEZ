from django.urls import path
from . import views


urlpatterns = [
  path('', views.get_file, name='get_file'),
  path('upload/', views.upload_file, name='upload_file'),
  path('download/', views.download_file, name='download_file'),
  path('download/secure/', views.secure_download, name='secure_download'),
]