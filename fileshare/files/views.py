from django.shortcuts import render
from django.http import JsonResponse
from .models import File, File_User
from django.views.decorators.csrf import csrf_exempt
from user.views import is_logged_in
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