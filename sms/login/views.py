from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from django.contrib.auth.models import User, auth
from django.contrib import messages
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('/user')
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        passwd = request.POST['password']
        path = request.POST['path']

        user = auth.authenticate(username=uname, password=passwd)

        if user is not None:
            auth.login(request,user)
            if path == '':
                return redirect('/user')
            else:
                return redirect(path)
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('/login')

    else:
        return render(request, 'login.html')
        

def register(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 == pass2:
            if User.objects.filter(username=uname).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email is already registered')
                return redirect('register')
            else:
                user = User.objects.create_user(username=uname, email=email, password=pass1, first_name=fname, last_name=lname)
                user.save()
                return redirect('login')
        else:
                messages.info(request, 'password mismatch')
                return redirect('register')

    else:
        return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
