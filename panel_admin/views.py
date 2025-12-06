from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from . import models
from wallet import models as wallet_models
from transactions.services import send_money_service, cash_out_service ,payment_service,transaction_history_service
from  transactions import models as transaction_models
from .permissions import IsPanelAdminAuthenticated
# from . import serializers
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        employee_id = request.data.get('employee_id')
        password = request.data.get('password')
        try:
            admin = models.PanelAdmin.objects.get(employee_id=employee_id)
            if admin.password == password:
                request.session['panel_admin_id'] = admin.id  # mark logged in
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except models.PanelAdmin.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsPanelAdminAuthenticated])
def transaction_history_view(request):
    if request.method == 'GET':
        trx_list = transaction_models.Transaction.objects.all().order_by('-transaction_time')[:10]
        history_list = []
        for trx in trx_list:
            history_list.append({
                "transaction_id": trx.transaction_id,
                "sender": trx.sender.account_number,
                "receiver": trx.receiver.account_number,
                "amount": str(trx.amount),
                "transaction_type": trx.transaction_type,
                "transaction_time": trx.transaction_time,
                "status": trx.status,
            })
        return Response({"history": history_list}, status=status.HTTP_200_OK)
