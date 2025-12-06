from django.db import models
from users.models import User
from wallet.models import Wallet
import random
import uuid

class Transaction(models.Model):
    trasaction_type=(
        ('sendmoney','SendMoney'),
        ('cashin','CashIn'),
        ('cashout','CashOut'),
        ('payment','Payment'),
        
    )
    status_choices=(
        ('pending','Pending'),
        ('completed','Completed'),
        ('failed','Failed'),
    )
    
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver')
    sender_wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE,related_name='sender_wallet')
    receiver_wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE,related_name='receiver_wallet')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=trasaction_type)
    transaction_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=status_choices, default='pending',null=True,blank=True)

    transaction_id = models.CharField(max_length=15, primary_key=True)


    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_unique_transaction_id()
        super().save(*args, **kwargs)

    # @staticmethod
    def generate_unique_transaction_id(self):
        """
        Generates a random 6-digit transaction_id and ensures uniqueness.
        """
          # local import to avoid circular dependency
        while True:
            txn_id = uuid.uuid4().hex[:10].upper()
            transaction_id = 'TX' + txn_id
            
            if not Transaction.objects.filter(transaction_id=transaction_id).exists():
                return transaction_id

    def __str__(self):
        return f"{self.transaction_id}"
    
    
    

# Create your models here.
