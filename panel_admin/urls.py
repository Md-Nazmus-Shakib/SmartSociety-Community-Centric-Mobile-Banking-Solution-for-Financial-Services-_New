from django.contrib import admin
from django.urls import path,include
from .import views
urlpatterns = [
    path('login/',views.login_view,name='admin-login'),
    path('moneyrequests/',views.list_pending_requests,name='admin-money-requests'),
    path('approve-request/<int:req_id>/',views.approve_request,name='admin-approve-request'),
    path('reject-request/<int:req_id>/',views.reject_request,name='admin-reject-request'),
    path('adminbalance/',views.admin_balance_view,name='admin-balance'),
    path('adminrevenue/',views.admin_revenue_view,name='admin-revenue'),
    path('usershistory/',views.profile_view,name='admin-user-history'),
    path('transactions/',views.transaction_history_view,name='admin-transaction-history'),
]