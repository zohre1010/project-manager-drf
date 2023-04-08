from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.views import APIView
from .models import Task,Project
from .serializers import *
from rest_framework.response import Response
from accounts_app.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status,generics
from accounts_app.permissions import IsAdminOrReadOnly,IsAdminOrIsManger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from datetime import timedelta, datetime
from rest_framework import filters
from rest_framework.generics import GenericAPIView
# -------------------------------------------------------------------------------------
# start of projects
class ProjectListView(LoginRequiredMixin,generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializers
    permission_classes = (IsAdminOrIsManger,)


class ProjectListViewForOneUser(LoginRequiredMixin, APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        project=Project.objects.filter(Q(created_by=user)|Q(members__id=str(user.id)))
        print(project)
        serializer_data= ProjectListSerializers(instance=project,many=True)        
        if user.id == request.user.id:
            return Response(data= serializer_data.data)
        return Response({'permission_denied' : "شما اجازه ی مشاهده ندارید"})

class ProjectCreateView(LoginRequiredMixin,APIView):
    permission_classes = (IsAdminOrIsManger,)
    def post(self, request):
        ser_data=ProjectCreateSerializers(data=request.data)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data,request)
            return Response(ser_data.data,status=status.HTTP_200_OK)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)

class ProjectUpdateView(LoginRequiredMixin,generics.UpdateAPIView):
    permission_classes = (IsAdminOrIsManger,)
    queryset = Project.objects.all()
    serializer_class = ProjectUpdateserializers
    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == "current":
            return self.request.user        
        return super(ProjectUpdateView, self).get_object()


class ProjectDeleteView(LoginRequiredMixin,APIView):
    permission_classes = (IsAdminOrIsManger,)
    queryset=Project.objects.all()
    def delete(selt,request,pk=None):
        Project=get_object_or_404(selt.queryset,pk=pk)
        Project.delete()
        return Response({"MSG": "پروژه حذف شد "},status=status.HTTP_204_NO_CONTENT)

# end of projects

# _________________________________________________________________________________________________________

# start of tasks

class TaskListViewForOneUser(LoginRequiredMixin, APIView):
   

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        task=Task.objects.filter(to_user=user)        
        serializer_data= TaskSerializers(instance=task,many=True)
        if user.id == request.user.id:
            return Response(data= serializer_data.data)        
        return Response({'permission_denied' : "شما اجازه ی مشاهده ندارید"})
   
class TaskOfTheProject(LoginRequiredMixin,APIView):
    permission_classes = (IsAdminOrIsManger,)
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        task=Task.objects.filter(project=project)
        serializer_data= TaskSerializers(instance=task,many=True)
        return Response(data= serializer_data.data)


class TaskCreateView(LoginRequiredMixin,APIView):
    permission_classes = (IsAdminOrIsManger,)
    def post(self, request):       
        ser_data=TaskCreateSerializers(data=request.data) 
       
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data,status=status.HTTP_200_OK)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)


class TaskUpdateView(LoginRequiredMixin,generics.UpdateAPIView):
    permission_classes = (IsAdminOrIsManger,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializers
    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == "current":
            return self.request.user        
        return super(TaskUpdateView, self).get_object()


class TaskUpdateForUser(LoginRequiredMixin,generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializers
    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == "current":
            return self.request.user        
        return super(TaskUpdateForUser, self).get_object()
        
class TaskDeleteView(LoginRequiredMixin,APIView):
    permission_classes = (IsAdminOrIsManger,)
    queryset=Task.objects.all()
    def delete(selt,request,pk=None):
        task=get_object_or_404(selt.queryset,pk=pk)
        task.delete()
        return Response({"MSG": "وظیفه حذف شد"},status=status.HTTP_204_NO_CONTENT) 


class DoingTaskView(LoginRequiredMixin,APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        doing=Task.objects.filter(to_user=user,
            created_at__lte=datetime.now(),
            end_at__gte=datetime.now())        
        serializer_data = TaskSerializers(instance=doing,many=True)
        if user.id == request.user.id:
            return Response(data= serializer_data.data)        
        return Response({'permission_denied' : "شما اجازه ی مشاهده ندارید"})


class LateTaskView(LoginRequiredMixin,APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        late=Task.objects.filter(to_user=user,
            end_at__lte=datetime.now())        
        serializer_data = TaskSerializers(instance=late,many=True)
        if user.id == request.user.id:
            return Response(data= serializer_data.data)        
        return Response({'permission_denied' : "شما اجازه ی مشاهده ندارید"})

class DoneTaskView(LoginRequiredMixin,APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        done=Task.objects.filter(to_user=user,
            status__contains={'title':True})
        serializer_data = TaskSerializers(instance=done,many=True)
        if user.id == request.user.id:
            return Response(data= serializer_data.data)        
        return Response({'permission_denied' : "شما اجازه ی مشاهده ندارید"})


# end of tasks
# _____________________________________________________________________________

class PercentTask(APIView):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        task=Task.objects.filter(project=project)
        total=task.count()
        users=User.objects.filter(project_member=project)
        data=[]    
        for user in users:
            task_user=Task.objects.filter(to_user=user,project=project).count()
            percent=(100*task_user)/total
            print(task_user,percent)
            context={
                'user':user.id,
                'percent':percent
            }
            data.append(context)
            print(data)
        return HttpResponse (data)

# _____________________________________________________________________________________
class NoteCreateView(LoginRequiredMixin,APIView):
    def post(self, request):             
        ser_data=NoteSerializers(data=request.data)    
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data,request)
            return Response(ser_data.data,status=status.HTTP_200_OK)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)

  
class NoteOfTheProjectView(LoginRequiredMixin,APIView):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        note=Note.objects.filter(project=project)
        serializer_data= NoteListSerializers(instance=note,many=True)
        return Response(data= serializer_data.data)

# _____________________________________________________________________________________


class ProjectListSearchView(LoginRequiredMixin, GenericAPIView):
    filter_backends = [filters.SearchFilter]
    search_fields = ['title','description']
    ordering_fields = ['id']
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        project=Project.objects.filter(Q(created_by=user)|Q(members__id=str(user.id)))
        task=Task.objects.filter(to_user=user)
        
        title = request.query_params.get('title')
        
        if title is not None:
            task = task.filter(title=title).distinct()
            project = project.filter(Q(title=title)| Q(description=title)).distinct()

        serializer_data= ProjectListSerializers(instance=project,many=True)
        ser_data=TaskSerializers(instance=task,many=True)
        if project:
            if user.id == request.user.id:
                return Response(data=serializer_data.data)
            return Response({'permission_denied' : "شما اجازه ی مشاهده ندارید"})
        elif task:
            if user.id == request.user.id:
                return Response(data=ser_data.data)
            return Response({'permission_denied' : "شما اجازه ی مشاهده ندارید"})
        else:
            return Response({'permission_denied' : "موردی پیدا نشد"})