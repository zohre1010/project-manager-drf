# Generated by Django 4.1.4 on 2023-01-11 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0013_user_limit_project'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='limit_project',
            new_name='limit',
        ),
    ]
