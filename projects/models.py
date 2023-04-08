from django.db import models
from accounts_app.models import User
# Create your models here.
from django.db.models import Q


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    members=models.ManyToManyField(User, blank=True,related_name='project_member')
    created_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(null=True,blank=True)
    end_at = models.DateTimeField(null=True,blank=True)
    

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=255,unique=True)
    project=models.ForeignKey(Project,on_delete=models.CASCADE, related_name='tasks')
    status=models.JSONField(default=dict)
    to_user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='task_to_user')
    created_at = models.DateTimeField(null=True,blank=True)
    end_at = models.DateTimeField(null=True,blank=True)


    def __str__(self):
        return self.title

class Note(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='note_user')
    project=models.ForeignKey(Project,on_delete=models.CASCADE, related_name='notes')
    text= models.CharField(max_length=120,unique=True)

    def __str__(self):
        return self.text