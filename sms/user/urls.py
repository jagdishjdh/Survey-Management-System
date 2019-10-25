from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('editor/', views.editor, name='editor'),
    path('preview/', views.preview, name='preview'),
]
