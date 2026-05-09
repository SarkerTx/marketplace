from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/customer/', views.CustomerRegisterView.as_view(), name='customer_register'),
    path('register/vendor/', views.VendorRegisterView.as_view(), name='vendor_register'),
    
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]