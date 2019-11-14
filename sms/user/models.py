from django.db import models
from django.contrib.auth.admin import User
# Create your models here.

# textarr = ["Short Ans ","Paragraph","Multiple choice",
#         "Checkboxes","Drop-down","File upload","Linear scale",
#         "Multiple choice grid","Tick box grid","Date","Time"]

# 1
class Survey(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    desc = models.TextField()
    createDate = models.DateTimeField(auto_now_add=True)
    endDate = models.DateTimeField(blank=True, null=True, default=None)
    anonymous = models.BooleanField(default=True)
    allowedUser = models.ManyToManyField(User)
    # isopen = models.BooleanField(default=True)

# 2
class Section(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    section_no = models.IntegerField()
    title = models.CharField(max_length=100)
    desc = models.TextField()

# 3
class User_survey(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    owner = models.BooleanField(default=True)
    # can add other columns related to permissions

# 4
class Question(models.Model):
    section = models.ForeignKey(Section,on_delete=models.CASCADE)
    desc = models.TextField()
    q_type = models.IntegerField()
    # valid_type = models.CharField(max_length=100,default=None) # alphanumaric, numaric, range, email, .pdf
    # other = models.BooleanField(default=False)
    required = models.BooleanField()

# 5
class Options(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.TextField()

# 6
# class Ques_options(models.Model):
    # question = models.ForeignKey(Question,on_delete=models.CASCADE)
    # option = models.ForeignKey(Options, on_delete=models.CASCADE)

# 7
class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.ForeignKey(Options, on_delete=models.CASCADE)
    other_text = models.TextField()
    # file = models.FileField

# class Ques_types