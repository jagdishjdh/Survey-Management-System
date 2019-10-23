from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='user_dashboard'),
    path('editor/', views.editor, name='user_editor'),
    path('preview/', views.preview, name='user_preview'),
]
