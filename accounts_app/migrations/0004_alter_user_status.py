# Generated by Django 4.1.4 on 2022-12-19 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0003_alter_user_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.JSONField(default=[]),
        ),
    ]