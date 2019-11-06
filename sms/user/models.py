from django.db import models
from django.contrib.auth.admin import User
# Create your models here.

# 1
class Survey(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    desc = models.TextField()
    createDate = models.DateTimeField(auto_now_add=True)
    endDate = models.DateTimeField(blank=True, null=True, default=None)
    isopen = models.BooleanField(default=True)
    anonymous = models.BooleanField(default=True)
    # other field like who can fill up this form
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
    q_type = models.CharField(max_length=100)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.ForeignKey(Options, on_delete=models.CASCADE)
    other_text = models.TextField()

# class Ques_types