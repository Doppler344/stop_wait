from django.contrib.auth.models import User, Group
from rest_framework import serializers

from teacherapi.models import Student, Teacher, Category, Subscription, Visit, Queue


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'email', 'groups', 'is_superuser', 'is_staff', 'pk']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ['url', 'user', 'first_name', 'last_name', 'middle_name', 'education_group', 'year_of_university']


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Teacher
        fields = ['url', 'user', 'first_name', 'last_name', 'middle_name', 'department', 'faculty', 'grade']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['url', 'name', 'student']


class SubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscription
        fields = ['url', 'student', 'teacher']


class VisitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Visit
        fields = ['url', 'teacher', 'office', 'datetime']


class QueueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Queue
        fields = ['url', 'student', 'visit', 'number', 'status']
