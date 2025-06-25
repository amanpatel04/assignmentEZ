from django.http import JsonResponse, HttpResponse
from .models import FileUser
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings

import jwt
import uuid

def get_user(request):
  return JsonResponse({'user': 'Aman Pate'}, safe=False)

@csrf_exempt
def register_user(request):
  if (request.method == 'POST'):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    is_ops = request.POST['is_ops']
    is_ops = True if is_ops == 'true' else False

    user = FileUser(first_name=first_name, last_name=last_name, email=email, password=password, is_ops=is_ops)
    user.run_on_create_function()
    user.save()
    
    return JsonResponse({'message': 'User created', 'data' : {'id': user.id}}, safe=False)
  else:
    return JsonResponse({'message': 'Only POST method is allowed', 'data' : {},}, safe=False)

@csrf_exempt
def login_user(request):
  if (request.method == 'POST'):
    email = request.POST['email']
    password = request.POST['password']
    user = FileUser.objects.filter(email=email).first()
    if user and user.check_password(password):
      token = jwt.encode({'id': str(user.id)}, settings.SECRET_KEY, algorithm='HS256')
      response = HttpResponse()
      response.set_cookie(key='token', value=token, httponly=True)
      return response
  return JsonResponse(status=400, data={'success':False}, safe=False)

def logout_user(request):
  response = HttpResponse()
  response.delete_cookie('token')
  return response

def is_logged_in(token):
  try:
    id = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    pk = uuid.UUID(id['id'])
    user = FileUser.objects.filter(id=pk).first()
    if not user:
        return None
    return user
  except Exception as e:
    print("JWT decode error:", e)
    return None


def send_verification_email(email, token):
    link = f"http://127.0.0.1:8000/verify/{token}"
    subject = 'Verify Your Email Address'
    message = f'Click the link to verify your account: {link}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

