# Generated by Django 4.1.4 on 2023-01-07 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_project_created_at_alter_project_end_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]