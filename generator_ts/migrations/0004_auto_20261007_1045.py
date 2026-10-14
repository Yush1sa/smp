from django.db import migrations

def create_default_roles(apps, schema_editor):
    Role = apps.get_model('generator_ts', 'Role')

    ROLES = [
        (0, "Не определено"),
        (1, "Заказчик"),
        (2, "Менеджер"),
        (3, "Исполнитель"),
    ]

    for role_id, role_name in ROLES:
        Role.objects.get_or_create(id=role_id, defaults={'name': role_name})


def remove_default_roles(apps, schema_editor):
    Role = apps.get_model('generator_ts', 'Role')
    Role.objects.filter(id__in=[0, 1, 2, 3]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('generator_ts', '0003_role_remove_profile_role_profile_roles'),
    ]

    operations = [
        migrations.RunPython(create_default_roles, reverse_code=remove_default_roles),
    ]
