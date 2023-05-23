from django.contrib import admin

from teacherapi.models import Student, Teacher, Category, Subscription, Visit, Queue, Department, Faculty

# Register your models here.
for model in Student, Teacher, Category, Subscription, Visit, Queue, Department, Faculty:
    admin.site.register(model)
