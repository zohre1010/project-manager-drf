from django.db import models
from accounts_app.models import User
# Create your models here.

class Meta(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='meta_user')
    meta_key=models.CharField(max_length=74)
    meta_value=models.JSONField(default=dict)
    created=  models.DateTimeField(null=True,blank=True)

    class Meta:
        get_latest_by= ['created']

    def __str__(self):
        return self.meta_key