# Generated by Django 4.1.4 on 2022-12-19 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0002_user_is_phone_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.JSONField(default={}),
        ),
    ]
