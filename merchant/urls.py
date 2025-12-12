from django.urls import path
from .import views
urlpatterns = [
    path('profile/', views.merchant_profile_view, name='merchant-profile'),
    path('transactions/', views.transaction_history_view, name='merchant-transaction-history'),
    path('cashout/',views.cashout_view ,name='merchant-cashout'),
    path('addproduct/',views.add_product_view ,name='merchant-add-product'),
    path('products/',views.list_products_view ,name='merchant-list-products'),
   
    
]