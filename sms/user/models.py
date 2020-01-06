
from django.db import models
from django.contrib.auth.admin import User
from datetime import datetime
# Create your models here.

# 1
class Survey(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    createDate = models.DateTimeField(auto_now_add=True)
    endDate = models.DateTimeField(blank=True, null=True, default=None)
    anonymous = models.BooleanField(default=True)

# 2
class Section(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    section_no = models.IntegerField()
    title = models.CharField(max_length=100)
    desc = models.TextField()
    # next_sec

# 3
class User_survey(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    owner = models.BooleanField(default=True)
    add_collab = models.BooleanField(default=True)

# 4
class Question(models.Model):
    section = models.ForeignKey(Section,on_delete=models.CASCADE)
    title = models.TextField()
    desc = models.TextField(null=True)
    qtype = models.IntegerField()
    order = models.IntegerField()
    required = models.BooleanField()
    other = models.BooleanField()
    image = models.ImageField(null=True, upload_to='question_image')
    constraint = models.TextField(null=True)

# 5
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.TextField()
    image = models.ImageField(upload_to='option_image')

# 6
class Row(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.TextField()

# 7
class Response(models.Model):
    response_time = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    row = models.ForeignKey(Row, on_delete=models.CASCADE, null=True)
    other = models.TextField(null=True)
    file = models.FileField(upload_to='response_files', null=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    options = models.TextField(null=True)

# 8
# class Response_options(models.Model):
#     response = models.ForeignKey(Response,on_delete=models.CASCADE)
#     selected_opt = models.ForeignKey(Option,on_delete=models.CASCADE)