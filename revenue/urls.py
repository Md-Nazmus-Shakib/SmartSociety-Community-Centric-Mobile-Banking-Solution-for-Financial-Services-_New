from . import views
from django.urls import path

urlpatterns = [
    path('revenue/', views.get_revenue, name='get_revenue'),
]