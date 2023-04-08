from django.db import models
from accounts_app.models import User
from projects.models import Project
# Create your models here.

class Conversazione(models.Model):
    from_user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='notif_from_user')
    to_user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='notif_to_user')
    message=models.TextField(blank=True, null=True)
    last_pm=models.TextField(blank=True, null=True)
    project=models.ForeignKey(Project,on_delete=models.CASCADE, related_name='project_ticket', blank=True, null=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_ticket', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    attachments=models.FileField(upload_to="file/",blank=True, null=True,default=None)
    state=models.JSONField(default=dict,blank=True, null=True)

    class Meta:
        ordering=('created',)
        get_latest_by = ['created']

class Channel(models.Model):
    image=models.ImageField(upload_to="channel/",null=True,blank=True)
    name=models.CharField(max_length=24,default='Mychannel')
    admin=models.ForeignKey(User,on_delete=models.CASCADE, related_name='admin_user')
    members=models.ManyToManyField(User, related_name='member_channel')
    created=models.DateTimeField(auto_now_add=True)
    last_pm=models.TextField(blank=True, null=True)
    state=models.JSONField(default=dict,blank=True, null=True)
    


class Message(models.Model):
    from_user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='message_from_user')
    channel=models.ForeignKey(Channel,on_delete=models.CASCADE, related_name='channel_message')
    attachments=models.FileField(upload_to="file/",blank=True, null=True,default=None)
    message=models.TextField(blank=True, null=True)
    created=models.DateTimeField(auto_now_add=True)
    