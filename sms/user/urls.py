from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('editor/<sur_id>', views.editor, name='editor get/post'),
    path('editprofile/', views.edit_profile, name='edit profile'),
    path('preview/<sur_id>', views.preview, name='preview'),
    path('response/<sur_id>', views.response, name='response'),
    path('get_csv/<sur_id>', views.get_csv, name='csv file'),
    path('create/', views.create_survey, name='create new survey'),
    path('submitted/', views.submitted, name='submitted'),
    path('delete/<sur_id>', views.delete_survey, name='delete a survey'),
    path('collab/<sur_id>', views.collab, name='collaboators'),
]
