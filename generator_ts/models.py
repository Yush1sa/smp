from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Role(models.Model):
    class Choices(models.IntegerChoices):
        UNDEFINED = 0, "Не определено"
        CUSTOMER = 1, "Заказчик"
        MANAGER = 2, "Менеджер"
        EXECUTOR = 3, "Исполнитель"

    id = models.IntegerField(primary_key=True, choices=Choices)
    name = models.CharField(max_length=50, editable=False)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, null=True, blank=True)
    roles = models.ManyToManyField(Role, blank=True, verbose_name="Роли")

    def __str__(self):
        return self.user.username if self.user else f"Profile {self.id}"


@receiver(post_save, sender=User)
def on_user_create(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)

        undefined_role, _ = Role.objects.get_or_create(
            id=Role.Choices.UNDEFINED
        )

        profile.roles.add(undefined_role)

# Create your models here.
class Project(models.Model):
    title = models.TextField("Название проекта")
    dbeg = models.DateField("Дата начала проекта")
    dend = models.DateField("Дата конца проекта")
    manager = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, related_name="manager_marks")
    customer = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, related_name="customer_marks")
    structure_code = models.IntegerField("Код структуры")
    kosgu = models.IntegerField("КОСГУ")
    kps = models.IntegerField("КПС")
    summ_application = models.IntegerField("Сводная заявка")
    funding_article = models.TextField("Статья финансирования")
    reflect_method = models.TextField("Способ отражения")

    def __str__(self):
        return self.title

class ProjectStage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    stage_number = models.SmallIntegerField("Номер этапа")
    title = models.TextField("Название этапа")
    executor_deadline = models.DateField("Срок выполнения этапа")
    customer_deadline = models.DateField("Срок приёмки результата")
    result = models.TextField("Результат этапа")
    material_result = models.TextField("Материальные носители этапа")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "stage_number"],
                name="unique_stage_number",
            )
        ]

    def __str__(self):
        return self.title

class StageTask(models.Model):
    stage = models.ForeignKey(ProjectStage, on_delete=models.CASCADE, null=True)
    task_number = models.SmallIntegerField("Номер задачи")
    executor = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True)
    cost = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField("Содержание задачи")
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["stage", "task_number"],
                name="unique_task_number",
            )
        ]