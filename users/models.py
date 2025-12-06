from django.db import models
from django.contrib.auth.models import AbstractUser
import random

USER_ROLES = (
        ('admin','Admin'),
        ('agent','Agent'),
        ('merchant','Merchant'),
        ('customer','Customer'),
    )

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    email = models.EmailField(unique=False)
    # authenticate by account_number instead of username
    USERNAME_FIELD = 'account_number'
    role = models.CharField(max_length=20, choices=USER_ROLES, blank=True, null=True)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    # balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    account_number = models.CharField(max_length=30, unique=True,primary_key=True)
    
    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_unique_account_number()
        super().save(*args, **kwargs)

    # @staticmethod
    def generate_unique_account_number(self):
        """
        Generates a random 6-digit account number and ensures uniqueness.
        """
          # local import to avoid circular dependency
        while True:
            ac_number = str(random.randint(100000, 999999))
            if self.role == 'admin':
                account_number = 'ad' + ac_number
            elif self.role == 'agent':
                account_number = 'A' + ac_number
            elif self.role == 'merchant':
                account_number = 'M' + ac_number
            elif self.role == 'customer':
                account_number = 'C' + ac_number
            else:
                account_number = 'S' + ac_number  # U for Unknown role
            if not User.objects.filter(account_number=account_number).exists():
                return account_number


    
    
    def __str__(self):
        return f"{self.username} - {self.account_number}"
# Create your models here.
