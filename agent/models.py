from django.db import models
from users.models import User
from wallet.models import Wallet

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'agent',primary_key=True,db_column='account_number')
    def __str__(self):
        return f"{self.user.username} - {self.user.account_number}"