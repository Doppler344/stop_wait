from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Student(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    education_group = models.CharField(max_length=10)
    year_of_university = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.middle_name} {self.education_group} {self.year_of_university}'


class Teacher(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    department = models.CharField(max_length=120, blank=True)
    faculty = models.CharField(max_length=120, blank=True)
    grade = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.middle_name} {self.grade} {self.department} {self.faculty}'


class Category(BaseModel):
    student = models.ManyToManyField(Student)
    NAME_CHOICES = (
        ('Экзамен', 'Экзамен'), ('Курсовая', 'Курсовая'), ('Лабораторная', 'Лабораторная'), ('Дипломная', 'Дипломная'),
        ('Другое', 'Другое'), ('Неизвестно', 'Неизвестно'))
    name = models.CharField(max_length=20, choices=NAME_CHOICES, default='Неизвестно')

    def __str__(self):
        return f'{self.pk} {self.name}'


class Subscription(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.teacher} {self.student}'


class Visit(BaseModel):
    datetime = models.DateTimeField()
    office = models.CharField(max_length=30)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, blank=True)  # Возможно не должно быть пустым

    def __str__(self):
        return f'{self.teacher} {self.office} {self.datetime}'


class Queue(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    WAITING = 'Ожидает'
    ENTERED = 'Зашел'
    LEFT = 'Вышел'
    SKIP = 'Пропустил'
    STATUS_CHOICES = ((WAITING, 'Ожидает'), (ENTERED, 'Зашел'), (LEFT, 'Вышел'), (SKIP, 'Пропустил'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=WAITING)

    def __str__(self):
        return f'{self.visit} {self.number} {self.status} {self.student}'
