# Generated by Django 4.1.4 on 2023-01-24 07:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0018_note_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversazione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, null=True)),
                ('last_pm', models.TextField(blank=True, null=True)),
                ('is_reply', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('attachments', models.JSONField(blank=True, default=dict, null=True)),
                ('state', models.JSONField(blank=True, default=dict, null=True)),
                ('is_read', models.BooleanField(default=False)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notif_from_user', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_ticket', to='projects.project')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_ticket', to='massages.conversazione')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notif_to_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
                'get_latest_by': ['created'],
            },
        ),
    ]
