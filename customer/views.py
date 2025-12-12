from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from . import models
from products import serializers as product_serializers
from wallet import models as wallet_models
from products import models as product_models
from transactions.services import send_money_service, cash_out_service ,payment_service,transaction_history_service
from . import serializers
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_profile_view(request):
    if request.method == 'GET':
        serializer = serializers.CustomerSerializer(request.user.customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_money_view(request):
    if request.method == 'POST':
        
        sender_ac_no = request.user.account_number
        reciver_ac_no = request.data.get('reciver_ac_no')
        amount = request.data.get('amount') 
        password = request.data.get('password')
        service_response = send_money_service(sender_ac_no, reciver_ac_no, amount, password)
        return Response(service_response,status=service_response.get("status", 200))
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cash_out_view(request):
    if request.method == 'POST':
        sender_ac_no = request.user.account_number
        reciver_ac_no = request.data.get('agent_ac_no')
        amount = request.data.get('amount') 
        password = request.data.get('password')
        service_response = cash_out_service(sender_ac_no, reciver_ac_no, amount, password)
        return Response(service_response,status=service_response.get("status", 200))    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment_view(request):
    if request.method == 'POST':
        sender_ac_no = request.user.account_number
        reciver_ac_no = request.data.get('merchant_ac_no')
        amount = request.data.get('amount') 
        password = request.data.get('password')
        service_response = payment_service(sender_ac_no, reciver_ac_no, amount,password)
        return Response(service_response,status=service_response.get("status", 200))    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history_view(request):
    if request.method == 'GET':
       user_ac_no = request.user.account_number
       service_response = transaction_history_service(user_ac_no)
       return Response(service_response,status=service_response.get("status", 200))
   
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_products_view(request):
    if request.method == 'GET':
        products = product_models.Product.objects.all()
        serializer = product_serializers.ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)