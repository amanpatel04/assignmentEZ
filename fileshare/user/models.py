from django.db import models
import uuid
import bcrypt
import base64

class FileUser(models.Model):
  id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  email = models.EmailField(max_length=50)
  password = models.CharField(max_length=256)
  is_verified = models.BooleanField(default=False)
  is_ops = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def run_on_create_function(self):
    hashed_pw = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
    self.password = base64.b64encode(hashed_pw).decode('utf-8')

  def check_password(self, password):
    hashed_pw_bytes = base64.b64decode(self.password)
    return bcrypt.checkpw(password.encode('utf-8'), hashed_pw_bytes)


  
