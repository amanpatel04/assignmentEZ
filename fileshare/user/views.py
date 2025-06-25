from django.http import JsonResponse, HttpResponse
from .models import FileUser
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache

import jwt
import uuid
import base64
import secrets

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
      response.status_code = 200
      response.data = {'message': 'User logged in', 'data' : {'id': user.id}}
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



def generate_base64_token(length=48):
  token_bytes = secrets.token_bytes(length)
  token_b64 = base64.urlsafe_b64encode(token_bytes).decode('utf-8')
  return token_b64.rstrip('=')


def send_verification_email(request):
  if request.COOKIES.get('token') == None:
    return JsonResponse(status=400, data={'message': 'User not logged in'}, safe=False)
  user = is_logged_in(request.COOKIES['token'])
  if user.is_verified == True:
    return JsonResponse({'message': 'User already verified', 'data' : {'id': user.id}}, safe=False)
  secret = generate_base64_token()
  print(secret)
  payload = {
    'id': str(user.id),
    'secret': secret
  }

  cache.set(secret, user.id, 300)
  token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

  link = f"http://127.0.0.1:8000/api/v1/user/verify/{token}"
  subject = 'Verify Your Email Address'
  message = f'Click the link to verify your account: {link}'
  send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

  return JsonResponse({'message': 'Verification email sent', 'data' : {'id': user.id}}, safe=False)


def verify_user(request, token):
  try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    id = uuid.UUID(payload['id'])
    if cache.get(payload['secret']) == None:
      return JsonResponse(status=400, data={'message': 'Invalid token'}, safe=False)
    user = FileUser.objects.filter(id=id).first()
    user.is_verified = True
    user.save()
    return JsonResponse({'message': 'User verified', 'data' : {'id': user.id}}, safe=False)
  except Exception as e:
    print("JWT decode error:", e)
    return JsonResponse({'message': 'Invalid token', 'data' : {}}, safe=False)