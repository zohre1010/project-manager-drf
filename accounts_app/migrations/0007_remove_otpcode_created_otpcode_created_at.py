# Generated by Django 4.1.4 on 2022-12-19 08:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0006_user_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otpcode',
            name='created',
        ),
        migrations.AddField(
            model_name='otpcode',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
