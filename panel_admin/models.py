from django.db import models
from users.models import User

# Create your models here.
class PanelAdmin(models.Model):
    
    username = models.CharField(max_length=150)
    employee_id = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username