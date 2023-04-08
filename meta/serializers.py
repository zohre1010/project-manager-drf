from rest_framework import serializers
from accounts_app.models import User
from datetime import timedelta, datetime
from .models import Meta

class NotifSerializers(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only=True)
    class Meta:
        model=Meta
        fields=['meta_value','created']
    def create(self, validated_data,request):
        meta_value=validated_data.get('meta_value')
        notif=Meta.objects.create(user=request.user,meta_key='notif',meta_value=meta_value)           
            
        validated_data['notif'] = notif
        return validated_data

class ReportSerializers(serializers.ModelSerializer):
    class Meta:
        model=Meta
        fields='__all__'