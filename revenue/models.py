from django.db import models

# Create your models here.
from django.db import models
from users.models import User 

class Revenue(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='revenue', primary_key=True,db_column='account_number')
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
   

    def __str__(self):
        return f"{self.user.username} - {self.user.account_number}"



# Create your models here.
