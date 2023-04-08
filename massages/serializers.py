from rest_framework import serializers
from .models import Project
from accounts_app.models import User
from .models import Conversazione ,Channel,Message
from datetime import timedelta, datetime
from collections import OrderedDict
from meta.models import Meta
import json
class CustomRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        model = self.queryset.model
        return model.objects.get(id=data)

class TicketListSerializers(serializers.ModelSerializer):
    class Meta:
        model=Conversazione
        fields=['id','from_user','to_user','message','is_reply']


class TicketSerializers(serializers.ModelSerializer):
    from_user= serializers.PrimaryKeyRelatedField(read_only=True,required=False)
    created = serializers.DateTimeField(read_only=True)
    class Meta:
        model=Conversazione
        fields=['from_user','to_user','message','created']

    
        
class TicketUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model=Conversazione
        fields=['state']
    
# ___________________________________________________________________________________________________________________
class ChatCreateSerializers(serializers.ModelSerializer):
    from_user= serializers.PrimaryKeyRelatedField(read_only=True)   
    created = serializers.DateTimeField(read_only=True)
    class Meta:
        model=Conversazione
        fields=['from_user','to_user','created']

    def create(self, validated_data,request):
        to_user=validated_data.get('to_user')
        chat=Conversazione.objects.create(from_user=request.user,to_user=to_user,created=datetime.now(),state={'active': True,'block':False,'delete':False,'status':'chat'})
        
        validated_data['chat'] = chat
        validated_data['from_user']=chat.from_user
        validated_data['created']=chat.created
        return validated_data

class SendMessageSerializers(serializers.ModelSerializer):
    # attachments=serializers.ListField(required=False,child=serializers.FileField())
    from_user= serializers.PrimaryKeyRelatedField(read_only=True) 
    to_user= serializers.PrimaryKeyRelatedField(read_only=True)  
    attachments=serializers.FileField(required=False)
    message= serializers.CharField(required=False,style={'base_template': 'textarea.html'})
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model=Conversazione
        fields=['from_user','to_user','message','attachments','created']

class ListConversazioneSerializers(serializers.ModelSerializer):
    to_user= serializers.PrimaryKeyRelatedField(read_only=True) 
    created = serializers.DateTimeField(read_only=True)
    class Meta:
        model=Conversazione
        fields=['to_user','last_pm','created']

# ____________________________________________________________________________________________________


class ChannelCreateSerializers(serializers.ModelSerializer):
    members=CustomRelatedField(many=True, queryset=User.objects.all())
    admin= CustomRelatedField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model=Channel
        fields=['name','admin','members','created','image']

    def create(self, validated_data,request):
        name=validated_data.get('name')
        members=validated_data.get('members')
        image=validated_data.get('image')
        channel=Channel.objects.create(image=image,name=name,admin=request.user,created=datetime.now(),state={'is_group':False,'delete':False,'is_read':False,'private':False})
        channel.members.set(members)
        channel.members.add(request.user)          
        channel.save()
        validated_data['channel'] = channel
        return validated_data

class MessageCreateSerializers(serializers.ModelSerializer):
    attachments=serializers.FileField(required=False)
    message= serializers.CharField(required=False,style={'base_template': 'textarea.html'})
    created = serializers.DateTimeField(read_only=True)
    from_user=CustomRelatedField(read_only=True)

    class Meta:
        model=Message
        fields=['from_user','message','attachments','created']


class ListChannelSerializers(serializers.ModelSerializer):
    class Meta:
        model=Channel
        fields=['name','last_pm']

class ChannelSerializers(serializers.ModelSerializer):
    name=serializers.CharField(required=False)
    members=CustomRelatedField(required=False,many=True, queryset=User.objects.all())
    admin= CustomRelatedField(read_only=True,required=False)
    image=serializers.FileField(required=False)
    class Meta:
        model=Channel
        fields=['admin','image','name','members','state','remove_members']


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.state = validated_data.get('state', instance.state)
        members=validated_data.get('members', instance.members)
        
        for member in members:
            instance.members.add(member.pk)       
        
        instance.save()
        print('instance')
        print(instance)
        return instance
    
class RemoveMemberSerializers(serializers.ModelSerializer):
    members=CustomRelatedField(required=False,many=True, queryset=User.objects.all())
    class Meta:
        model=Channel
        fields=['members']
    def update(self, instance, validated_data):
        members=validated_data.get('members', instance.members)
        
        for member in members:
            instance.members.remove(member.pk)
        
        instance.save()
        print('instance')
        print(instance)
        return instance