from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from . import models
from wallet import models as wallet_models
from revenue import models as revenue_models
from customer import models as customer_models
from merchant import models as merchant_models
from products import models as product_models
from agent import models as agent_models
from . import serializers
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
import logging
import re
security_logger = logging.getLogger("security_logger")
pattern = r'^[a-zA-Z0-9]+@[a-z]+\.edu+\.bd$'
mobile_pattern = r'^01[3-9][0-9]{8}$'
# new_pattern = r'^1/2/3$'


@api_view(['POST'])
def  user_registration_view(request):
    if request.method == 'POST':
        serializer = serializers.UserSerializer(data=request.data)
        email = request.data.get('email','')
        mobile_number = (request.data.get('mobile_no',''))
        if not (re.fullmatch(pattern,email)):
            security_logger.info(f"Account creation failed - Invalid email format: {email}")
            return Response({'error': 'Invalid email format. Only @diu.edu.bd domains are allowed.'}, status=status.HTTP_400_BAD_REQUEST)
        # re.sub(new_pattern,mobile_pattern,mobile_number)
        if (re.fullmatch(mobile_pattern,mobile_number) is None):
            security_logger.info(f"Account creation failed - Invalid mobile number format: {mobile_number}")
            return Response({'error': 'Invalid mobile number format. It should be a valid BD phone number and contain 11 digits.'}, status=status.HTTP_400_BAD_REQUEST)
            
        if serializer.is_valid():
            serializer.save()
            if serializer.data.get('role')  in ['customer','merchant','agent']:
                wallet_models.Wallet.objects.create(user=serializer.instance)
            
                
            if serializer.data.get('role') == 'customer':
                customer_models.Customer.objects.create(user=serializer.instance)
            elif serializer.data.get('role') == 'merchant':
                merchant_models.Merchant.objects.create(user=serializer.instance)
                
            elif serializer.data.get('role') == 'agent':
                agent_models.Agent.objects.create(user=serializer.instance)
                revenue_models.Revenue.objects.create(user=serializer.instance)
            security_logger.info(f"Account created successfully for account number: {serializer.data.get('account_number')}")  
            return Response(
                {
                    "message": "Account created successfully ",
                    "account_number":serializer.data.get('account_number')
                },
                        status=status.HTTP_201_CREATED)
        security_logger.info(f"Account creation failed with errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])    
def user_login_view(request):
    if request.method == 'POST':
        account_number = request.data.get('account_number') 
        password = request.data.get('password')
        try:
            user = models.User.objects.get(account_number=account_number)
            if user.check_password(password):
                serializer = serializers.UserSerializer(user)
                security_logger.info(f"Login successful for account number: {account_number}")
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                security_logger.info(f"Login failed for account number: {account_number} - Invalid credentials")
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except models.User.DoesNotExist:
            security_logger.info(f"Login failed - User with account number: {account_number} does not exist")
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
            
        
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail_view(request):
    if request.method == 'GET':
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method in ['PUT', 'PATCH']:
        serializer = serializers.UserSerializer(request.user, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def RefreshToken(refresh_token):
    raise NotImplementedError

@api_view(['PUT','PATCH'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    
    user = request.user #retunrs a single user object #filter returns multiple objects 
   

    if request.method in ['PUT', 'PATCH']:
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not user.check_password(old_password):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        if not new_password:
            return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def logout_view(request):
    refresh_token = request.data.get("refresh")
    if not refresh_token:
        return Response({'error': 'refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    except TokenError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

        
# Create your views here.
