from django.contrib import admin
from django.urls import path,include
from .import views
urlpatterns = [
    path('login/',views.login_view,name='admin-login'),
    path('transactions/',views.transaction_history_view,name='admin-transaction-history'),
]