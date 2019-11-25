from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import *
import re 
from datetime import datetime

class form:
     def __init__(self,survey,dic):
         self.survey = survey
         self.dictionary = dic

typearr = ["Short Ans", "Paragraph", "Multiple Choice",
        "Checkboxes", "Drop-down", "File Upload", "Linear scale",
        "Multiple choice grid", "Tick box grid", "Date", "Time"]

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

def edit_profile(request):
    if request.user.is_authenticated:
        user = request.user

        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']

            if (pass1 == "" and pass2 == "") or pass1 == pass2:
                if User.objects.filter(email=email).exclude(username=user.username).exists():
                    messages.info(request, 'email is already registered')
                    return redirect('/user/editprofile')
                else:
                    user.first_name = fname
                    user.last_name = lname
                    user.email = email
                    if pass1 != "":
                        user.set_password(pass1)
                    user.save()
                    messages.info(request,"Details Updated")
                    # return redirect('/user/editprofile')
            else:
                    messages.error(request, 'password mismatch')
                    return redirect('/user/editprofile')

        context = {'user': user}
        return render(request, 'edit_profile.html',context)
    else:
        messages.info(request, 'Please Login First')
        return render(request, 'login.html')

def create_survey(request):
    if request.user.is_authenticated:
        user1 = request.user
        new_sur = Survey(title="New One",desc="",endDate=None)
        new_sur.save()
        new_sec = Section(survey=new_sur,section_no=1,title="New Section",desc="")
        new_sec.save()
        User_survey(user=user1,survey=new_sur).save()
        return editor(request, new_sur.id)
    else:
        messages.info(request, 'Please Login First')
        return render(request, 'login.html')

def editor(request, sur_id=None):
    if sur_id is None:
        return redirect('/user')

    if request.user.is_authenticated:
        user = request.user
        sur = Survey.objects.filter(user_survey__user=user, id=sur_id)

        if sur.count() == 0:
            # means this survey does not belongs to the logged in user
            return redirect('/user')
        
        else:
            survey = sur[0]
            # if this is post request then data is to be saved first
            if request.method == 'POST':
                sp1 = ' #~# '
                sp2 = ' ## '
                sp3 = ' #@# '
                ques_update = request.POST['q_update'] # #~# , ##, #@#
                sec_update = request.POST['sec_update'] # #~# , ##
                sur_update = request.POST['sur_update'] # #~#
                ques_del = request.POST['q_del'] # ##
                sec_del = request.POST['sec_del'] # ##
                opt_del = request.POST['opt_del'] # ##

                print("****************************")
                print(sur_update)
                sur_upd_lst = re.split(" #~# ",sur_update)[:-1]
                survey.title = sur_upd_lst[0]
                survey.desc = sur_upd_lst[1]
                if sur_upd_lst[2] != "":
                    survey.endDate = datetime.strptime(sur_upd_lst[2], "%Y-%m-%dT%H:%M")
                else:
                    survey.endDate = None
                ano = False
                if sur_upd_lst[3] == 'true': 
                    ano = True
                survey.anonymous = ano
                survey.save()
                # print(survey.endDate)

                print("****************************")
                print(ques_del)
                if ques_del != "":
                    q_id_del = [int(x) for x in re.split(" ## ",ques_del)]
                    ques_lst_del = Question.objects.filter(id__in=q_id_del)
                    for q in ques_lst_del:
                        q.delete()

                print("****************************")
                print(sec_del)
                if sec_del != "":
                    sec_id_del = [int(x) for x in re.split(" ## ",sec_del)]
                    sec_lst_del = Section.objects.filter(id__in=sec_id_del)
                    for se in sec_lst_del:
                        se.delete()

                print("****************************")
                print(opt_del)
                if opt_del != "":
                    opt_id_del = [int(x) for x in re.split(" ## ",opt_del)]
                    opt_lst_del = Option.objects.filter(id__in=opt_id_del)
                    for op in sec_lst_del:
                        op.delete()

                print("****************************")
                print(sec_update)
                # id, sec_num, title, desc, next_sec(not yet present in model)
                sec_upd_lst = re.split(sp1,sec_update)[:-1]
                for i in range(len(sec_upd_lst)):
                    sec_upd_lst[i] = re.split(sp2,sec_upd_lst[i])
                # print(sec_upd_lst)

                for s in sec_upd_lst:
                    if s[0] == '-1':
                        new_sec = Section(survey=survey,title=s[2],desc=s[3],section_no=int(s[1]))
                        new_sec.save()
                    else:
                        sec = Section.objects.filter(id=int(s[0]))
                        sec.title = s[2]
                        sec.desc = s[3]
                        sec.section_no = int(s[1])
                        sec.save()


                print("****************************")
                print(ques_update)
                # id, sec_no, qtype, req(true/false), order, other(0/1), title, desc, constraint,
                #  [columns], [rows]
                ques_upd_lst = re.split(" #~# ",ques_update)[:-1]
                for i in range(len(ques_upd_lst)):
                    ques_upd_lst[i] = re.split(" ## ",ques_upd_lst[i])
                    ques_upd_lst[i][-2] = re.split(" #@# ",ques_upd_lst[i][-2])[:-1]
                    for k in range(len(ques_upd_lst[i][-2])):
                        ques_upd_lst[i][-2][k] = re.split(" #^# ",ques_upd_lst[i][-2][k])

                    ques_upd_lst[i][-1] = re.split(" #@# ",ques_upd_lst[i][-1])[:-1]
                    for k in range(len(ques_upd_lst[i][-1])):
                        ques_upd_lst[i][-1][k] = re.split(" #^# ",ques_upd_lst[i][-1][k])
                print(ques_upd_lst)

                for q in ques_upd_lst:
                    sec = Section.objects.filter(survey=survey,section_no=q[1])
                    req = False
                    if q[3] == 'true': 
                        req = True
                    oth = False
                    if q[5] == '1': 
                        oth = True

                    if q[0] == '-1':
                        ques = Question(section=sec,title=q[6],desc=q[7],q_type=int(q[2]),required=req,order=int(q[4]),other=oth)
                        ques.save()
                        
                    else:
                        ques = Question.objects.filter(id=int(q[0]))
                        ques.section = sec
                        ques.desc = q[7]
                        ques.title = q[6]
                        ques.q_type = int(q[2])
                        ques.required = req
                        ques.other = oth
                        ques.order = int(q[4])
                        ques.save()

                    for opt in q[7]:
                        if opt[0] == '-1':
                            op = Option(question=ques,value=opt[1])
                            op.save()
                        else:
                            op = Option.objects.filter(id=int(opt[0]))
                            op.value = opt[1]
                            op.save()

                print("****************************")


            sec_lst = Section.objects.filter(survey=survey)
            
            # creating form object to be sent to editor page
            dic = {}
            for sec in sec_lst:
                ques_lst = Question.objects.filter(section=sec)
                q_dic = {}

                for q in ques_lst:
                    opt_lst = Option.objects.filter(question=q)
                    q_dic[q] = list(opt_lst)
                
                dic[sec] = q_dic

            complete_survey = form(survey,dic)
            # form object created
            return render(request, 'editor.html', {'form':complete_survey})

    else:
        messages.info(request, 'Please Login First')
        return render(request, 'login.html')

def response(request, sur_id=None):
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
            resp = Response.objects.filter(survey=sur[0])
            ngr = "10#10#10#10##daskjfh#asldhfl#asdb#sah##adsf#asfd#fe#fsg##af#af#fe#fsg"
            gr = [[]]
            return render(request, 'response.html', {'non_grid_responses':ngr, 'grid_responses':gr,  'sur_id':sur[0].id})

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

def preview(request, sur_id=None):
    # if this is post request then data is to be saved first
    if sur_id is not None:
        try:
            survey = Survey.objects.get(id=sur_id)
            sec_lst = Section.objects.filter(survey=survey)
            
            # creating form object to be sent to editor page
            dic = {}
            for sec in sec_lst:
                ques_lst = Question.objects.filter(section=sec)
                q_dic = {}

                for q in ques_lst:
                    opt_lst = Option.objects.filter(question=q)
                    q_dic[q] = list(opt_lst)
                
                dic[sec] = q_dic

            complete_survey = form(survey,dic)
            # form object created
            return render(request, 'preview.html', {'form':complete_survey})

        except ObjectDoesNotExist:
            pass

    else:
        return redirect('/user')


def collab(request,sur_id=None):
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
            return render(request, 'collab.html')

    else:
        messages.info(request, 'Please Login First')
        return render(request, 'login.html')
