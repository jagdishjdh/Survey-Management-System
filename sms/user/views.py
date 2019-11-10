from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *

class form:
     def __init__(self,survey,dic):
         self.survey = survey
         self.dictionary = dic


# Create your views here.
def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        survey_lst = Survey.objects.filter(user_survey__user=user)
        # print(survey_lst)
        context = {'surveys': survey_lst}
        return render(request, 'dashboard.html',context)
    else:
        messages.info(request, 'Please Login First')
        return render(request, 'login.html')

def create_survey(request):
    if request.user.is_authenticated:
        user1 = request.user
        new_sur = Survey(title="New One",desc="",endDate=None)
        new_sur.save()
        new_sec = Section(survey=new_sur,section_no=1,title="",desc="")
        new_sec.save()
        User_survey(user=user1,survey=new_sur).save()
        return editor(request, new_sur.id)
    else:
        messages.info(request, 'Please Login First')
        return render(request, 'login.html')

def editor(request, sur_id=None):
    if sur_id == None:
        return redirect('/user')

    if request.method == 'POST':
        str1 = request.POST['input1']
        str2 = request.POST['input2']
        str3 = request.POST['input3']
        str4 = request.POST['input4']
        str5 = request.POST['input5']
        print('***************************************')
        print(str1)
        print('***************************************')
        print(str2)
        print('***************************************')
        print(str3)
        print('***************************************')
        print(str4)
        print('***************************************')
        print(str5)
        print('***************************************')        

    if request.user.is_authenticated:
        user = request.user
        # print(sur_id,'****************')
        sur = Survey.objects.filter(user_survey__user=user, id=sur_id)
        
        if sur.count() == 0:
            # means this survey does not belongs to the logged in user
            return redirect('/user')
        
        else:
            sec_lst = Section.objects.filter(survey=sur[0])
            
            # creating form object to be sent to editor page
            dic = {}
            for sec in sec_lst:
                ques_lst = Question.objects.filter(section=sec)
                q_dic = {}

                for q in ques_lst:
                    opt_lst = Options.objects.filter(question=q)
                    q_dic[q] = list(opt_lst)
                
                dic[sec] = q_dic

            complete_survey = form(sur[0],dic)
            # form object created
            return render(request, 'editor.html', {'form':complete_survey})

    else:
        messages.info(request, 'Please Login First')
        return render(request, 'login.html')

def delete_survey(request, sur_id=None):
    if sur_id == None:
        return redirect('/user')
    if request.user.is_authenticated:
        user = request.user
        # print(sur_id,'****************')
        sur = Survey.objects.filter(user_survey__user=user, id=sur_id)

        if sur.count() == 0:
            # means this survey does not belongs to the logged in user
            return redirect('/user')
        else:
            # messages.warning(request,"Are you sure to delete the selected Survey?")
            sur.delete()
            return redirect("/user")

    else:
        messages.info(request, 'Please Login First')
        return render(request, 'login.html')

def preview(request):
    pass
