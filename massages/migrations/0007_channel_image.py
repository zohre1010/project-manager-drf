# Generated by Django 4.1.4 on 2023-02-05 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('massages', '0006_channel_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='channel/'),
        ),
    ]
