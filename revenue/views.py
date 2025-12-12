from django.shortcuts import render
from . import models
from . import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_revenue(request):
    if request.method == 'GET':
        revenue = models.Revenue.objects.get(user=request.user)
        serializer = serializers.RevenueSerializer(revenue)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
