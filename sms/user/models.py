from django.db import models
from django.contrib.auth.admin import User
# Create your models here.

# user
# survey
# user_survey       // this will allow multiple user of a survey i.e. many-to-many relationship
# question
# survey_question   // allow reuse of question
# offered-answers   // 
# answers           // ? user_id ? survey_id ? question_id ? offered_ans_id ? other_text
# 
# 1
class Survey(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    desc = models.TextField()
    createDate = models.DateTimeField(auto_now_add=True)
    endDate = models.DateTimeField(default=False)
    isopen = models.BooleanField(default=True)
    anonymous = models.BooleanField(default=True)
    # other field like who can fill up this form
# 2
class Section(models.Model):
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    section_no = models.IntegerField()
    title = models.CharField(max_length=100)
    desc = models.TextField()

# 3
class User_survey(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    owner = models.BooleanField(default=True)
    # can add other columns related to permissions

# 4
class Question(models.Model):
    section_id = models.ForeignKey(Section,on_delete=models.CASCADE)
    desc = models.TextField()
    q_type = models.CharField(max_length=100)
    required = models.BooleanField()

# 5
class Options(models.Model):
    value = models.CharField(max_length=100)

# 6
class Ques_options(models.Model):
    q_id = models.ForeignKey(Question,on_delete=models.CASCADE)
    option_id = models.ForeignKey(Options, on_delete=models.CASCADE)

# 7
class Response(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    response_id = models.ForeignKey(Options, on_delete=models.CASCADE)
    other_text = models.TextField()

