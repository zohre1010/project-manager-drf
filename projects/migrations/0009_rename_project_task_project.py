# Generated by Django 4.1.4 on 2023-01-10 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_project_title_alter_task_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='Project',
            new_name='project',
        ),
    ]
