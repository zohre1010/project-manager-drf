# Generated by Django 4.1.4 on 2023-01-15 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.JSONField(default=dict),
        ),
    ]
