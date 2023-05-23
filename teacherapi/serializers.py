from django.contrib.auth.models import User, Group
from rest_framework import serializers

from teacherapi.models import Student, Teacher, Category, Subscription, Visit, Queue, Department, Faculty


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['pk', 'url', 'name']


class DepartmentSerializer(serializers.ModelSerializer):
    # faculty = FacultySerializer()
    class Meta:
        model = Department
        fields = ['pk', 'url', 'name', 'faculty']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'url', 'username', 'password', 'email', 'groups', 'is_superuser', 'is_staff']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['pk', 'url', 'name']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['pk', 'url', 'user', 'first_name', 'last_name', 'middle_name', 'education_group',
                  'year_of_university']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['pk', 'url', 'user', 'first_name', 'last_name', 'middle_name', 'department', 'grade']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'url', 'name', 'student']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['pk', 'url', 'student', 'teacher']


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ['pk',  'teacher', 'office', 'datetime_start', 'datetime_end']


class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ['pk', 'url', 'student', 'visit', 'number', 'status']
