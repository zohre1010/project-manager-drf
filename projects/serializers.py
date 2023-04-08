from rest_framework import serializers
from .models import Task,Project,Note
from accounts_app.models import User


class ProjectListSerializers(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields='__all__'

class CustomRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        model = self.queryset.model
        return model.objects.get(id=data)

class ProjectCreateSerializers(serializers.ModelSerializer):
    members=CustomRelatedField(many=True, queryset=User.objects.all())
    class Meta:
        model =Project
        fields=['title','description','members']

    def create(self, validated_data,request):
        title = validated_data.get('title')
        description = validated_data.get('description')
        members = validated_data.get('members')
        print(members)
        project = Project.objects.create(title=title,description=description,created_by= request.user)
        

        project.members.set(members)
        project.members.add(request.user)          
        project.save()
        validated_data['project'] = project
        return validated_data

    # def validate_members(self, attrs):
    #     members =attrs(members)
    #     print(members)
    #     all_user=User.objects.all()
    #     print(all_user) 
    #     check=all(item in all_user for item in members)
    #     print(check)
    #     if check is False:
    #         raise serializers.ValidationError('کاربر وجود ندارد')
    #     return attrs
    
class ProjectUpdateserializers(serializers.ModelSerializer):    
    class Meta:
        model = Project
        fields = ['title','description','members']
    
class TaskSerializers(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields='__all__'


class TaskCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model =Task
        fields='__all__'
    def create(self, validated_data):
        title = validated_data.get('title')
        project = validated_data.get('project')
        to_user = validated_data.get('to_user')
        created_at = validated_data.get('created_at')
        end_at = validated_data.get('end_at')
        
        user=User.objects.filter(id=to_user.id)
        limit=user.values('limit').first()['limit']
        status_user=user.values('status').first()['status']

        count=Task.objects.filter(to_user=to_user,status__contains={'title':False}).count()
        
        if count <  limit and status_user['is_active']==True:
            task = Task.objects.create(title=title,project=project,to_user= to_user,created_at=created_at,end_at=end_at,status={'title': False,'description':''})
       
            taskofproject=Task.objects.filter(project=project).first()
            for e in Task.objects.filter(project=project):
                e.project.created_at=taskofproject.created_at
                e.project.save()
            
            validated_data['task'] = task
            return validated_data
        raise serializers.ValidationError('کاربر مجاز به گرفتن وظیفه نیست')


class TaskUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields=['status']

    def update(self, instance, validated_data): 
        instance.status ={**instance.status, **validated_data.get('status', instance.status)}
        instance.save()
        return instance



class NoteSerializers(serializers.ModelSerializer):

    class Meta:
        model=Note
        fields=['project','text']

    def create(self, validated_data,request):
        project = validated_data.get('project')
        text = validated_data.get('text')
        
        note = Note.objects.create(project=project,text= text, user=request.user) 
        validated_data['note'] = note
        return validated_data
        

class NoteListSerializers(serializers.ModelSerializer):
    class Meta:
        model=Note
        fields='__all__'