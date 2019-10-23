from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='login_home'),
    path('login/', views.login, name='login_login'),
    path('register/', views.register, name='login_register'),
]
