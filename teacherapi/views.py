from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import views
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from rest_framework.response import Response
from rest_framework.request import Request

from teacherapi.serializers import (UserSerializer, GroupSerializer, StudentSerializer, TeacherSerializer,
                                    CategorySerializer, SubscriptionSerializer, VisitSerializer, QueueSerializer)

from teacherapi.models import Student, Teacher, Category, Subscription, Visit, Queue
from teacherapi.validation import validate_username


class UpdateQueueStatus(views.APIView):
    # Эта штука же есть уже в rest
    """Обновить свой статус в очереди"""
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request: Request):
        content = {'message': request.user.username,
                   'data': request.data}
        return Response(content)


class GetInVisit(views.APIView):
    """Записаться на прием"""
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request: Request):
        visit_id = request.data["visit_id"]
        user = request.user
        # Находим нужного студента и нужный прием
        visit = Visit.objects.get(pk=visit_id)
        student = Student.objects.get(user=user)

        # Проверяем, что студент не находиться уже в очереди
        queue = Queue.objects.filter(student=student, visit=visit_id)
        if queue.exists():
            content = {'message': 'Вы уже в очереди',  # вернем список, вдруг произошла смена места в очереди
                       'data': [{'number': el.number, 'status': el.status, 'username': user.username,
                                 'student': str(student)} for el in queue]}
            return Response(content)

        # Узнаем номер последнего в очереди
        queues_last_number = Queue.objects.filter(visit=visit_id).order_by('-number').first()
        if queues_last_number:
            queues_last_number = queues_last_number.number
        # Проверяем, что в очереди кто-то вообще есть
        else:
            queues_last_number = 0
        # Встаем за ним
        queues_last_number += 1
        queue = Queue(student=student, visit=visit, number=queues_last_number)
        queue.save()

        content = {'message': 'success',
                   'data': {'number': queue.number, 'status': queue.status, 'username': user.username,
                            'student': str(student)}}
        return Response(content)


class CreateUser(views.APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request: Request):
        try:
            validate_username(request.data["username"])
        except ValidationError as error:
            content = {'message': error.messages,
                       'data': request.data}
            return Response(content)

        try:
            validate_password(request.data["password"])
        except ValidationError as error:
            content = {'message': error.messages,
                       'data': request.data}
            return Response(content)

        user: User = User.objects.create_user(username=request.data["username"], password=request.data["password"])
        content = {'message': 'success',
                   'data': {'user': {'pk': user.pk, 'username': user.username}}}
        return Response(content)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]


class StudentViewSet(viewsets.ModelViewSet):
    # Должен быть доступен студенту для
    # - создания своего профиля
    # - изменения только своего профиля
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeacherViewSet(viewsets.ModelViewSet):
    # Должен быть доступен преподавателю для
    # - создания своего профиля
    # - изменения только своего профиля
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    # Должен быть доступен студенту для
    # - создания своих категорий
    # - изменения своих категорий
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class SubscriptionViewSet(viewsets.ModelViewSet):
    # Должен быть доступен студенту для
    # - создания своих подписок
    # - изменения своих подписок
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class VisitViewSet(viewsets.ModelViewSet):
    # Должен быть доступен преподавателю для
    # - создания своих мероприятий
    # - изменения своих мероприятий
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    permission_classes = [permissions.IsAuthenticated]



class QueueViewSet(viewsets.ModelViewSet):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
