# Generated by Django 4.2.5 on 2025-01-21 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_usuario_endereco_alter_usuario_nif_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.CharField(max_length=500),
        ),
    ]
