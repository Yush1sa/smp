from typing import Any

from django.contrib.messages.api import success
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from rest_framework.decorators import action

from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate

from generator_ts.models import *
from generator_ts.serializers import ProjectsSerializer, ProjectStageSerializer, StageTaskSerializer


class ProjectsViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer

class ProjectStageViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = ProjectStage.objects.all()
    serializer_class = ProjectStageSerializer

class StageTaskViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = StageTask.objects.all()
    serializer_class = StageTaskSerializer

class ProfileViewSet(GenericViewSet):
    queryset = User.objects.all()

    @action(detail=False, url_path='me', methods=['get'])
    def get_me(self, request, *args, **kwargs):
        data : dict[str, Any] = {
            'is_authenticated': self.request.user.is_authenticated
        }

        if self.request.user.is_authenticated:
            data.update({
                "username": self.request.user.username,
                "id": self.request.user.id,
                "roles": list(self.request.user.profile.roles.values_list('name', flat=True))
            })


        return Response(data=data)

    @action(detail=False, url_path='logout', methods=['POST'])
    def logout(self, *args, **kwargs):
        django_logout(self.request)

        return Response()

    @action(detail=False, url_path="login", methods=['POST'])
    def login(self, *args, **kwargs):
        username = self.request.data['username']
        password = self.request.data['password']

        success = False
        status_code = 403

        user = authenticate(username=username, password=password)
        if user:
            success = True
            status_code = 200
            django_login(self.request, user)

        return Response({
            'success': success
        }, status=status_code)