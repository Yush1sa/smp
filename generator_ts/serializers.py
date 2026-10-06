from rest_framework import serializers

from generator_ts.models import Project, ProjectStage, StageTask

class ProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'dbeg', 'dend']


class ProjectStageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectStage
        fields = '__all__'


class StageTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageTask
        fields = '__all__'