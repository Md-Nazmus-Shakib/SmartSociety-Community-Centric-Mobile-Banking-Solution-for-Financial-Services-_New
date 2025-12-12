from django.shortcuts import render
from . import models
from . import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from users.models import User

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wallet(request):
    if request.method == 'GET':
        wallet = models.Wallet.objects.get(user=request.user)
        serializer = serializers.WalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_wallet_by_account(request):
    """Return wallet info for a given account_number query parameter.
    Example: /api/wallet/balance/?account_number=admin7777
    """
    acct = request.query_params.get('account_number')
    if not acct:
        return Response({'detail': 'account_number required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(account_number=acct)
    except User.DoesNotExist:
        return Response({'detail': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
    try:
        wallet = models.Wallet.objects.get(user=user)
    except models.Wallet.DoesNotExist:
        return Response({'detail': 'wallet not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = serializers.WalletSerializer(wallet)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Create your views here.
