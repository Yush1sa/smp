from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

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