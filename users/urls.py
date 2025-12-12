
from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.user_registration_view, name='user-registration'),
    path('login/', views.user_login_view, name='user-login'),
    path('logout/',views.logout_view,name='user-logout'),
    path('profile/', views.user_profile_view, name='user-profile'),
    path('edit/', views.user_detail_view, name='user-detail'),
   
    path('change-password/',views.change_password_view, name='change-password'),
]
