from django.shortcuts import render

# Create your views here.
def dashboard(request):
    # check if someone is loged in or not
    # if not then ask to login
    # else return dashboard page
    return render(request, 'dashboard.html')

def editor(request):
    pass

def preview(request):
    pass
