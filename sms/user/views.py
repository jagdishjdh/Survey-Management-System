from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import *
import re, csv
from datetime import datetime


class form:
     def __init__(self,survey,dic):
         self.survey = survey
         self.dictionary = dic

typearr = [[0,"Short Ans"], [1,"Paragraph"],[2,"Multiple Choice"],
        [3,"Checkboxes"], [4,"Drop-down"], [5,"File Upload"], [6,"Linear scale"],
        [7,"Multiple choice grid"], [8,"Tick box grid"], [9,"Date"], [10,"Time"]]

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
        # new_sec = Section(survey=new_sur,section_no=1,title="New Section",desc="")
        # new_sec.save()
        User_survey(user=user1,survey=new_sur).save()
        return redirect('/user/editor/'+str(new_sur.id))
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
                row_del = request.POST['row_del'] # ##

                # print("****************************")
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

                print("******qdellllllllllll**********************")
                print(ques_del)
                if ques_del != "":
                    q_id_del = [int(x) for x in re.split(" ## ",ques_del)[:-1]]
                    ques_lst_del = Question.objects.filter(id__in=q_id_del)
                    for q in ques_lst_del:
                        q.delete()

                print("**********secdellllllllllllllll******************")
                print(sec_del)
                if sec_del != "":
                    sec_id_del = [int(x) for x in re.split(" ## ",sec_del)[:-1]]
                    sec_lst_del = Section.objects.filter(id__in=sec_id_del)
                    for se in sec_lst_del:
                        se.delete()

                print("**********optdellllllll******************")
                print(opt_del)
                if opt_del != "":
                    opt_id_del = [int(x) for x in re.split(" ## ",opt_del)[:-1]]
                    opt_lst_del = Option.objects.filter(id__in=opt_id_del)
                    for op in opt_lst_del:
                        op.delete()

                print("*******rowdelllllllllllll*********************")
                print(row_del)
                if row_del != "":
                    row_id_del = [int(x) for x in re.split(" ## ",row_del)[:-1]]
                    row_lst_del = Row.objects.filter(id__in=row_id_del)
                    for op in row_lst_del:
                        op.delete()

                # print("****************************")
                # print(sec_update)
                # id, sec_num, title, desc, next_sec(not yet present in model)
                sec_upd_lst = re.split(sp1,sec_update)[:-1]
                for i in range(len(sec_upd_lst)):
                    sec_upd_lst[i] = re.split(sp2,sec_upd_lst[i])
                # print(sec_upd_lst)

                for s in sec_upd_lst:
                    print("secsecsecsecsecccccccccccccccccc")
                    print(sec_upd_lst)
                    if s[0] == '-1':
                        new_sec = Section(survey=survey,title=s[2],desc=s[3],section_no=int(s[1]))
                        new_sec.save()
                    else:
                        sec = Section.objects.filter(id=int(s[0]))[0]
                        sec.title = s[2]
                        sec.desc = s[3]
                        sec.section_no = int(s[1])
                        sec.save()


                print("********qqqqqqq********************")
                print(ques_update)
                # id, sec_no, qtype, req(true/false), order, other(0/1), title, desc, constraint,
                #  [columns], [rows]
                ques_upd_lst = re.split(" #~# ",ques_update)[:-1]
                for i in range(len(ques_upd_lst)):
                    ques_upd_lst[i] = re.split(" ## ",ques_upd_lst[i])
                    ques_upd_lst[i][-2] = re.split(" #@# ",ques_upd_lst[i][-2])[:-1]
                    for k in range(len(ques_upd_lst[i][-2])):
                        ques_upd_lst[i][-2][k] = re.split(" #&# ",ques_upd_lst[i][-2][k])

                    ques_upd_lst[i][-1] = re.split(" #@# ",ques_upd_lst[i][-1])[:-1]
                    for k in range(len(ques_upd_lst[i][-1])):
                        ques_upd_lst[i][-1][k] = re.split(" #&# ",ques_upd_lst[i][-1][k])

                print(ques_upd_lst)
                for q in ques_upd_lst:
                    sec = Section.objects.filter(survey=survey,section_no=q[1])[0]
                    req = False
                    if q[3] == 'true': 
                        req = True
                    oth = False
                    if q[5] == '1': 
                        oth = True

                    if q[0] == '-1':
                        ques = Question(section=sec,title=q[6],desc=q[7],qtype=int(q[2]),required=req,order=int(q[4]),other=oth,constraint=q[8])
                        ques.save()
                        
                    else:
                        ques = Question.objects.filter(id=int(q[0]))[0]
                        ques.section = sec
                        ques.desc = q[7]
                        ques.title = q[6]
                        ques.qtype = int(q[2])
                        ques.required = req
                        ques.other = oth
                        ques.order = int(q[4])
                        ques.constraint=q[8]
                        ques.save()

                    for opt in q[9]:
                        if opt[0] == '-1':
                            op = Option(question=ques,value=opt[1])
                            op.save()
                            print(opt,'aaaaaaaaaa')
                        else:
                            op = Option.objects.filter(id=int(opt[0]))[0]
                            op.value = opt[1]
                            op.save()

                    for row in q[10]:
                        if row[0] == '-1':
                            op = Row(question=ques,value=row[1])
                            op.save()
                            print(row,'aaaaaaaaaa')
                        else:
                            op = Row.objects.filter(id=int(row[0]))[0]
                            op.value = row[1]
                            op.save()

                print("****************************")

                return redirect('/user/editor/'+str(survey.id))

            sec_lst = Section.objects.filter(survey=survey).order_by('section_no')
            
            # creating form object to be sent to editor page
            dic = {}
            for sec in sec_lst:
                ques_lst = Question.objects.filter(section=sec)
                q_dic = {}

                for q in ques_lst:
                    opt_lst = Option.objects.filter(question=q).order_by('id')
                    row_lst = Row.objects.filter(question=q).order_by('id')
                    q_dic[q] = (list(opt_lst),list(row_lst))
                # print(q_dic)
                dic[sec] = q_dic

            complete_survey = form(survey,dic)
            # form object created
            return render(request, 'editor.html', {'form':complete_survey, 'num_sec':len(sec_lst),'optlist':typearr})

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
            # qtype1#qtype2 ...##
            # qtitle1   qtitle2 ...
            # responses ...op1@op2
            ngr = ""
            gr = []
            # assuming all questions have different number in order
            questions = Question.objects.filter(section__survey=sur[0]).order_by('order')
            t11 = ''
            t22 = ''
            for q in questions:
                if q.qtype == 7 or q.qtype == 8:
                    pass
                else:
                    # ngr[0].append(q.qtype)
                    # ngr[1].append(q.title)
                    t11 = t11 + str(q.qtype)+' # '
                    t22 = t22 + q.title+' # '
            ngr = t11[:-3] + ' ## ' + t22[:-3]

            resps = Response.objects.filter(survey=sur[0]).exclude(question__qtype__in=[7,8]).order_by('response_num','question__order')
            responses78 = Response.objects.filter(survey=sur[0],question__qtype__in=[7,8]).order_by('response_num','row')
            resp78title = Response.objects.filter(survey=sur[0],question__qtype__in=[7,8]).distinct('question__order','row').order_by('question__order','row')
            
            # anonymous = sur[0].anonymous

            temp_resp_num = resps[0].response_num
            temp_response = ''
            for resp in resps:
                if resp.response_num != temp_resp_num:
                    ngr = ngr + ' ## ' + temp_response[:-3]
                    temp_response = ''
                    temp_resp_num = resp.response_num

                # short & long answer type
                if resp.question.qtype in [0,1]:
                    temp_response = temp_response + resp.other + ' # '
                    # options type
                elif resp.question.qtype in [2,3,4]:
                    if resp.options == "":
                        temp_response = temp_response + resp.other + ' # '
                    else:
                        op_ids = [int(x) for x in re.split(" @ ",resp.options)[:-1]]
                        t = ''
                        for op_id in op_ids:
                            t = t + Option.objects.filter(id=op_id).value + ' @ '
                        t = t[:-3]
                        temp_response = temp_response + t + ' # '
                    # file upload type
                elif resp.question.qtype == 5:
                    temp_response = temp_response + resp.file.url + ' # '
                    # linear scale type
                elif resp.question.qtype == 6:
                    temp_response = temp_response + resp.other + ' # '
                    # grid type
                elif resp.question.qtype in [7,8]:
                    pass
                    # date type
                elif resp.question.qtype == 9:
                    temp_response = temp_response + str(resp.date) + ' # '
                    # time type
                elif resp.question.qtype == 10:
                    temp_response = temp_response + str(resp.time) + ' # '
                else:
                    pass
            
            ngr = ngr + ' ## ' + temp_response[:-3]

            try:
                gr_temp = ''
                temp_num = resp78title[0].question.order
                for respitem in resp78title:
                    if respitem.question.order != temp_num:
                        # add all responses to gr_temp
                        gr_temp = gr_temp[:-3]

                        cur_q_res = responses78.filter(question__order=temp_num)
                        temp_resp_num = cur_q_res[0].response_num
                        temp_response = ''
                        for resp in cur_q_res:
                            if resp.response_num != temp_resp_num:
                                gr_temp = gr_temp + ' ## ' + temp_response[:-3]
                                temp_response = []
                                temp_resp_num = resp.response_num

                            op_ids = [int(x) for x in re.split("@",resp.options)]
                            t = ''
                            for op_id in op_ids:
                                t = t + Option.objects.filter(id=op_id).value + '@'
                            t = t[:-1]
                            temp_response = temp_response + t + ' # '
                        
                        gr_temp = gr_temp + ' ## ' + temp_response[:-3]
                        gr.append(gr_temp)
                        gr_temp = ''
                        temp_num = respitem.question.order

                    
                    gr_temp = gr_temp + respitem.question.title+'['+respitem.row.value+']' + ' # '

            except:
                pass
            
            print(ngr)
            print(gr)

            return render(request, 'response.html', {'non_grid_responses':ngr,
                    'grid_responses':gr , 'sur_id':sur[0].id})

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

        isowner = User_survey.objects.filter(user=user,survey=sur[0])[0].owner
        if isowner:
            # messages.warning(request,"Are you sure to delete the selected Survey?")
            sur.delete()
            return redirect("/user")
        else:
            return redirect('/user')

    else:
        messages.info(request, 'Please Login First')
        return render(request, 'login.html')


# response_num = 1

def preview(request, sur_id=None):
    # if this is post request then data is to be saved first
    if sur_id is not None:
        try:
            survey = Survey.objects.get(id=sur_id)

            if request.method == 'POST':
                response_num = int(datetime.now().strftime('%Y%m%d%H%M%s'))

                answers = request.POST['text_answer']
                answers = re.split(' ## ',answers)[:-1]
                for i in range(len(answers)):
                    answers[i] = re.split(' # ', answers[i])
                
                for ans in  answers:
                    new_res = Response(response_num=response_num,
                            survey=survey,
                            question=Question.objects.get(id=int(ans[0])),
                            options=ans[2])
                    typ = int(ans[1])
                    if typ == 9:
                        try:
                            new_res.date = datetime.strptime(ans[3], "%Y-%m-%d")
                        except:
                            pass
                    elif typ == 10:
                        try:
                            new_res.time = datetime.strptime(ans[3], "%H:%M")
                        except:
                            pass
                    elif typ == 5:
                        pass
                    elif typ == 6:
                        pass
                    else:
                        new_res.other = ans[3]
                    
                    new_res.save()

                return redirect('/user/submitted/')


            sec_lst = Section.objects.filter(survey=survey)
            
            # creating form object to be sent to editor page
            dic = {}
            for sec in sec_lst:
                ques_lst = Question.objects.filter(section=sec)
                q_dic = {}

                for q in ques_lst:
                    opt_lst = Option.objects.filter(question=q).order_by('id')
                    row_lst = Row.objects.filter(question=q).order_by('id')
                    q_dic[q] = [list(opt_lst),list(row_lst)]
                
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
            users_sur = User_survey.objects.filter(survey=sur[0])
            if request.method == 'POST':
                new_coll = request.POST['user']
                try:
                    addcollab = request.POST['addcollab']
                    addcollab = True
                except:
                    addcollab = False
                # try:
                #     owner = request.POST['owner1']
                #     owner = True
                # except:
                owner = False
                    
                # print(new_coll,addcollab,owner)
                if users_sur.filter(user__username=new_coll).count() == 0:
                    new = User_survey(user=User.objects.get(username=new_coll),survey=sur[0],owner=owner,add_collab=addcollab)
                    new.save()
                else:
                    temp = users_sur.filter(user__username=new_coll)[0]
                    temp.owner = owner
                    temp.add_collab = addcollab
                    temp.save()

            all_users = User.objects.all().exclude(username=user.username).values('username')
            # print(type(all_users[0]))
            users_sur = User_survey.objects.filter(survey=sur[0])

            return render(request, 'collab.html',
                {'cur_user':users_sur.filter(user=user)[0],'users':users_sur,'all_username':list(all_users),'sur_id':sur_id})

    else:
        messages.info(request, 'Please Login First')
        return render(request, 'login.html')

def get_csv(request,sur_id=None):
    if sur_id == None:
        return redirect('/user')
    if request.user.is_authenticated:
        user = request.user
        # print(sur_id,'****************')
        sur = Survey.objects.filter(user_survey__user=user, id=sur_id)

        if sur.count() == 0:
            # means this survey does not belongs to the logged in user
            return redirect('/user')

        # now create the csv file

    else:
        messages.info(request, 'Please Login First')
        return render(request, 'login.html')


def submitted(request):
    return render(request,'submitted.html')