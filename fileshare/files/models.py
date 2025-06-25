from django.db import models

class File(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=100)
  file = models.FileField(upload_to='files/')

class File_User(models.Model):
  user = models.ForeignKey('user.FileUser', on_delete=models.CASCADE)
  file = models.ForeignKey('files.File', on_delete=models.CASCADE)

