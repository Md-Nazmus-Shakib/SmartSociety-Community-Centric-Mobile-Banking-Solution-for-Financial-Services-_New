from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from . import models
from wallet import models as wallet_models
from transactions.services import send_money_service, cash_out_service ,payment_service,transaction_history_service,cashin_service
from . import serializers
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def agent_profile_view(request):
    if request.method == 'GET':
        serializer = serializers.AgentSerializer(request.user.agent)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cashin_view(request):
    if request.method == 'POST':
        sender_ac_no = request.user.account_number
        reciver_ac_no = request.data.get('customer_ac_no')
        amount = request.data.get('amount') 
        service_response = cashin_service(sender_ac_no, reciver_ac_no, amount)
        return Response(service_response,status=service_response.get("status", 200))
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history_view(request):
    if request.method == 'GET':
       user_ac_no = request.user.account_number
       service_response = transaction_history_service(user_ac_no)
       return Response(service_response,status=service_response.get("status", 200))
