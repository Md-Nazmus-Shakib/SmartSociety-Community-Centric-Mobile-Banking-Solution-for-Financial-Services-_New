from . import models
from rest_framework import serializers

class RevenueSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    account_number = serializers.CharField(source='user.account_number', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    class Meta:
        model = models.Revenue
        fields = ['username','account_number','role', 'revenue', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at','revenue']
        
        
    