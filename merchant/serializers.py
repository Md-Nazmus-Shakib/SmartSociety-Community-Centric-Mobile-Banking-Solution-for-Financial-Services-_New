from rest_framework import serializers
from . import models

class MerchantSerializer(serializers.ModelSerializer):
   
    username = serializers.CharField(source='user.username',read_only= True)
    account_number = serializers.CharField(source='user.account_number', read_only=True)
    role = serializers.CharField(source='user.role',read_only=True)
    email = serializers.EmailField(source='user.email',read_only=True)
    mobile_no = serializers.CharField(source='user.mobile_no',read_only=True)
    wallet_balance = serializers.DecimalField(source='user.wallet.balance', max_digits=12, decimal_places=2, read_only=True)
    class Meta:
        model = models.Merchant
        fields = ['username', 'account_number', 'role', 'email', 'mobile_no', 'wallet_balance']