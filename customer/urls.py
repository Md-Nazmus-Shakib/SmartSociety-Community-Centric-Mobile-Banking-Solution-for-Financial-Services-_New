from django.urls import path
from .import views
urlpatterns = [
    path('profile/', views.customer_profile_view, name='customer-profile'),
    path('send-money/', views.send_money_view, name='customer-send-money'),
    path('cash-out/', views.cash_out_view, name='customer-cash-out'),
    path('payment/', views.payment_view, name='customer-payment'),
    path('viewproducts/', views.view_products_view, name='customer-view-products'),
    path('transaction/', views.transaction_history_view, name='customer-transaction-history'),
    # path('edit/', views.edit_view, name='customer-edit'),
]