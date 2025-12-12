from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from . import models
from wallet import models as wallet_models
from revenue import models as revenue_models
from transactions.models import MoneyRequest
from . import models
from transactions.services import send_money_service, cash_out_service ,payment_service,transaction_history_service
from  transactions import models as transaction_models
from .permissions import IsPanelAdminAuthenticated
# from . import serializers
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication
from django.db import transaction as db_transaction

@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        employee_id = request.data.get('employee_id')
        password = request.data.get('password')

        try:
            admin = models.PanelAdmin.objects.get(employee_id=employee_id)

            if admin.password == password:
                request.session['panel_admin_id'] = admin.id
                request.session.modified = True      # 🔥 IMPORTANT
                request.session.save()              # ensure session_key is created
                return Response({
                    "message": "Login successful",
                    "panel_admin_id": admin.id,
                    "session_key": request.session.session_key
                }, status=status.HTTP_200_OK)

            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        except models.PanelAdmin.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([AllowAny])
def transaction_history_view(request):
    if request.method == 'GET':
        trx_list = transaction_models.Transaction.objects.all().order_by('-transaction_time')
        history_list = []
        for trx in trx_list:
            history_list.append({
                "transaction_id": trx.transaction_id,
                "sender": trx.sender.account_number,
                "receiver": trx.receiver.account_number,
                "amount": str(trx.amount),
                "transaction_type": trx.transaction_type,
                "transaction_time": trx.transaction_time.isoformat() if trx.transaction_time else None,
                "status": trx.status,
            })
        return Response({"history": history_list}, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([AllowAny])
def list_pending_requests(request):
    # Check if logged-in user is a panel admin

    pending = MoneyRequest.objects.filter(status="PENDING").order_by("-created_at")

    data = [
        {
            "id": r.id,
            "agent": r.agent.username,
            "agent_account": r.agent.account_number,
            "amount": str(r.amount),
            "created_at": r.created_at.isoformat() if r.created_at else None
        }
        for r in pending
    ]

    return Response({"pending_requests": data})


@api_view(["POST"])
@permission_classes([IsPanelAdminAuthenticated])
def approve_request(request, req_id):
    try:
        req = MoneyRequest.objects.select_related("agent").get(id=req_id)
    except MoneyRequest.DoesNotExist:
        return Response({"error": "Request not found"}, status=status.HTTP_404_NOT_FOUND)
    if req.status != "PENDING":
        return Response({"error": "Request already processed"}, status=status.HTTP_400_BAD_REQUEST)

    agent_user = getattr(req.agent, "user", req.agent)

    with db_transaction.atomic():
        wallet = wallet_models.Wallet.objects.select_for_update().get(user=agent_user)
        adminwallet = wallet_models.Wallet.objects.select_for_update().get(user__account_number='admin7777')
        wallet.balance += req.amount
        adminwallet.balance -= req.amount
        adminwallet.save(update_fields=["balance"])
        wallet.save(update_fields=["balance"])

        req.status = "APPROVED"
        req.save(update_fields=["status"])

    return Response({"success": True, "message": "Request approved"}, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsPanelAdminAuthenticated])
def reject_request(request, req_id):
    

    try:
        req = MoneyRequest.objects.get(id=req_id)
    except MoneyRequest.DoesNotExist:
        return Response({"error": "Request not found"}, status=404)

    req.status = "REJECTED"
    req.save()

    return Response({"success": True, "message": "Request rejected"})
@api_view(['GET'])
@permission_classes([IsPanelAdminAuthenticated])
def admin_balance_view(request):
    if request.method == 'GET':
        try:
            admin_user = models.User.objects.get(account_number='admin7777')  # assuming admin user has this employee_id
            wallet = wallet_models.Wallet.objects.get(user=admin_user)
            return Response({"balance": str(wallet.balance)}, status=status.HTTP_200_OK)
        except models.PanelAdmin.DoesNotExist:
            return Response({'error': 'Admin user not found'}, status=status.HTTP_404_NOT_FOUND)
        except wallet_models.Wallet.DoesNotExist:
            return Response({'error': 'Wallet not found'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
@permission_classes([IsPanelAdminAuthenticated])
def admin_revenue_view(request):
    if request.method == 'GET':
        try:
            admin_user = models.User.objects.get(account_number='admin7777')  # assuming admin user has this employee_id
            revenue = revenue_models.Revenue.objects.get(user=admin_user)
            return Response({"revenue": str(revenue.revenue)}, status=status.HTTP_200_OK)
        except models.User.DoesNotExist:
            return Response({'error': 'Admin user not found'}, status=status.HTTP_404_NOT_FOUND)
        except revenue_models.Revenue.DoesNotExist:
            return Response({'error': 'Revenue record not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsPanelAdminAuthenticated])
def profile_view(request):
    if request.method == 'GET':
        try:
            users = models.User.objects.all()
            user_data = []
            for user in users:
                user_data.append({
                    "account_number": user.account_number,
                    "username": user.username,
                    "role": user.role,
                    "email": user.email,
                })
            return Response({"users": user_data}, status=status.HTTP_200_OK)
        except models.User.DoesNotExist:
            return Response({'error': 'Users not found'}, status=status.HTTP_404_NOT_FOUND)
