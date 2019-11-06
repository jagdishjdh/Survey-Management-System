from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('editor/<sur_id>', views.editor, name='editor'),
    path('preview/', views.preview, name='preview'),
    path('create/', views.create_survey, name='create new survey'),
    path('delete/<sur_id>', views.delete_survey, name='delete a survey'),
]
