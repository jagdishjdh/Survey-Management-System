from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Survey)
admin.site.register(Section)
admin.site.register(Question)
admin.site.register(Options)
admin.site.register(Response)

