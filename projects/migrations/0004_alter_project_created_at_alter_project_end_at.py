# Generated by Django 4.1.4 on 2023-01-04 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_alter_task_created_at_alter_task_end_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='end_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]