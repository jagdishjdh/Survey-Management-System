from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from django.contrib.auth.models import User, auth

# Create your views here.

def home(request):
    return HttpResponse('<h2>home</h2>')

def login(request):
    pass

def register(request):
    pass
