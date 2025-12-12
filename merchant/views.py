from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from . import models
from products.models import Product
from products.models import Product
from products import serializers as product_serializers
from wallet import models as wallet_models
from transactions.services import send_money_service, cash_out_service ,payment_service,transaction_history_service
from . import serializers
from rest_framework.decorators import api_view,permission_classes,authentication_classes,parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def merchant_profile_view(request):
    if request.method == 'GET':
        serializer = serializers.MerchantSerializer(request.user.merchant)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cashout_view(request):
    if request.method == 'POST':
        sender_ac_no = request.user.account_number
        reciver_ac_no = request.data.get('agent_ac_no')
        amount = request.data.get('amount') 
        password = request.data.get('password')
        service_response = cash_out_service(sender_ac_no, reciver_ac_no, amount, password)
        return Response(service_response,status=service_response.get("status", 200))
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history_view(request):
    if request.method == 'GET':
       user_ac_no = request.user.account_number
       service_response = transaction_history_service(user_ac_no)
       return Response(service_response,status=service_response.get("status", 200))
   
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def add_product_view(request):
    # Accept multipart/form-data (for image upload) and JSON
    if request.method != 'POST':
        return Response({'detail': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        merchant = request.user  # should be a User instance
        # Log request info for debugging
        print(f"add_product_view called by: {merchant} content_type={request.content_type}")

        # Pass request in context so serializer can build full URLs for image fields if needed
        serializer = product_serializers.ProductSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            product = serializer.save(merchant=merchant)   # single save; returns model instance
            out = product_serializers.ProductSerializer(product, context={'request': request}).data
            return Response(out, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as exc:
        import traceback
        traceback.print_exc()
        return Response({'detail': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_products_view(request):
    if request.method == 'GET':
        merchant = request.user
        products = Product.objects.filter(merchant=merchant)
        # include request in context so ImageField builds absolute URLs
        serializer = product_serializers.ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)