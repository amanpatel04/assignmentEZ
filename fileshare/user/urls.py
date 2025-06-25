from django.urls import path
from . import views


urlpatterns = [
  path('', views.get_user, name='get_user'),
  path('register/', views.register_user, name='register_user'),
  path('login/', views.login_user, name='login_user'),
  path('logout/', views.logout_user, name='logout_user'),
  path('gen/', views.send_verification_email, name='send_verification_email'),
  path('verify/<token>/', views.verify_user, name='verify_user'),
]