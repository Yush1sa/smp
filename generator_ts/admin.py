from django.contrib import admin

from generator_ts.models import Project, ProjectStage, StageTask


# Register your models here.
@admin.register(Project)
class Projects_admin(admin.ModelAdmin):
    list_display = ['id', 'title', 'dbeg', 'dend', 'manager', 'customer']

@admin.register(ProjectStage)
class Projects_stages_admin(admin.ModelAdmin):
    list_display = ['id', 'project', 'stage_number', 'title', 'executor_deadline', 'customer_deadline', 'result', "material_result"]


@admin.register(StageTask)
class Stage_tasks_admin(admin.ModelAdmin):
    list_display = ["id", 'stage', 'task_number', 'executor', 'cost', 'description']