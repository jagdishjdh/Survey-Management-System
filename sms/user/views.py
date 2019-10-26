from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *

# Create your views here.
def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        survey_lst = Survey.objects.filter(user_survey__user_id=user.id)
        context = {'surveys': survey_lst}
        return render(request, 'dashboard.html',context)
    else:
        messages.info(request, 'Please Login First')
        return render(request, 'login.html')


def editor(request):
    pass

def preview(request):
    pass
