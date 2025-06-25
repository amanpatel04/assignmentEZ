from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from .models import File, File_User
from django.views.decorators.csrf import csrf_exempt
from user.views import is_logged_in
from django.shortcuts import redirect
from django.conf import settings

import jwt
import os
# Create your views here.
def get_file(request):
  files = File.objects.all()
  return JsonResponse({'files': list(files.values())}, safe=False)

@csrf_exempt
def upload_file(request):
  if (request.method == 'POST'):
    name = request.POST['name']
    file = request.FILES['file']
    if (request.COOKIES.get('token') == None):
      return JsonResponse(status=400, data={'success':False}, safe=False)
    extension = file.name.split('.')[-1]
    if extension == 'docx' or extension == 'pptx' or extension == 'xlsx':
      user = is_logged_in(request.COOKIES['token'])
      if not user:
        return JsonResponse(status=400, data={'success':False}, safe=False)
      file = File.objects.create(name=name, file=file)
      File_User.objects.create(user=user, file=file)
      return JsonResponse({'success':True}, safe=False)
  return JsonResponse(status=400, data={'success':False}, safe=False)


def download_file(request):
  if (request.COOKIES.get('token') == None):
    return JsonResponse(status=400, data={'success':False}, safe=False)
  qurey = request.GET.get('file_id')
  file = File.objects.filter(id=qurey).first()
  user = is_logged_in(request.COOKIES['token'])
  payload = {
    'download_link' : file.file.url,
    'message': 'success'
  }
  token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
  url = request.build_absolute_uri('/api/v1/file/download/secure/?token=' + token)
  return redirect(url)


def secure_download(request):
  # if (request.GET.get('token') == None):
  #   return JsonResponse(status=400, data={'success':False}, safe=False)
  try:
    payload = jwt.decode(request.GET.get('token'), settings.SECRET_KEY, algorithms=['HS256'])
    file_path = os.path.join(settings.BASE_DIR, payload['download_link'][1:])
    if not os.path.exists(file_path):
      return JsonResponse(status=400, data={'message': 'File not found'}, safe=False)
    return FileResponse(open(file_path, 'rb'))
  except Exception as e:
    print("JWT decode error:", e)
    return JsonResponse(status=400, data={'success':False}, safe=False)