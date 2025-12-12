from django.urls import path
from .import views
urlpatterns = [
    path('profile/', views.agent_profile_view, name='agent-profile'),
    path('transactions/', views.transaction_history_view, name='agent-transaction-history'),
    path('cashin/',views.cashin_view ,name='agent-cashin'),
    path('requestmoney/',views.request_money ,name='agent-request-money'),
   
    
]