# Generated by Django 4.2.5 on 2024-12-20 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_usuario_groups_usuario_is_active_usuario_is_staff_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='user_permissions',
        ),
    ]
