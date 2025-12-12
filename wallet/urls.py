from . import views
from django.urls import path

urlpatterns = [
    path('wallet/', views.get_wallet, name='get_wallet'),
    path('balance/', views.get_wallet_by_account, name='get_wallet_by_account'),
]