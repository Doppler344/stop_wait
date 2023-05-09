from django.contrib import admin

from teacherapi.models import Student, Teacher, Category, Subscription, Visit, Queue

# Register your models here.
for model in Student, Teacher, Category, Subscription, Visit, Queue:
    admin.site.register(model)
