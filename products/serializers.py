from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    merchant_name = serializers.CharField(source='merchant.username', read_only=True)
    class Meta:
        model = Product
        exclude = ['merchant']