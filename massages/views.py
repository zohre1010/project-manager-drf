from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Project
from .serializers import *
from rest_framework.response import Response
from accounts_app.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status,generics
from accounts_app.permissions import IsAdminOrReadOnly,IsAdminOrIsManger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from datetime import timedelta, datetime
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from accounts_app.permissions import IsAdminOrReadOnly
from meta.models import Meta
import json
# Create your views here.

class TicketListView(LoginRequiredMixin,APIView):
    def get(self,request,pk):
        project = get_object_or_404(Project, pk=pk)
        ticket=Conversazione.objects.filter(project=project)
        serializer_data= TicketListSerializers(instance=ticket,many=True)
        return Response(data= serializer_data.data)

class TicketCreateView(LoginRequiredMixin,APIView):
    def post(self,request,project_id):
        project=get_object_or_404(Project,id=project_id)
        member=project.members.all()
        ser_data=TicketSerializers(data=request.data) 
        if ser_data.is_valid():
            to_user=ser_data.validated_data['to_user']
            if to_user in member:
                ser_data.save(from_user = request.user,project = project,state={'is_done':False})
                report=Meta.objects.create(user=request.user,meta_key='ticket',meta_value=ser_data.data)
                return Response(ser_data.data,status=status.HTTP_200_OK)
            return Response({"MSG": "کاربر در لیست اعضا وجود ندارد"})
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)


class TicketReplyView(LoginRequiredMixin,APIView):
    def post(self,request,project_id,ticket_id):
        project=get_object_or_404(Project,id=project_id)
        member=project.members.all()
        ticket = get_object_or_404(Conversazione, id=ticket_id)
        ser_data=TicketSerializers(data=request.data) 
        if ser_data.is_valid():
            i=ser_data.validated_data['to_user']
            if i in member:
                ser_data.save(from_user = request.user,project = project,reply = ticket,is_reply = True,state={'is_done':False, 'status':'ticket'})
                return Response(ser_data.data,status=status.HTTP_200_OK)
            return Response({"MSG": "کاربر در لیست اعضا وجود ندارد"})
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)

class ReplyForOneTicket(LoginRequiredMixin,APIView):
    def get(self,request,ticket_id):
        ticket = get_object_or_404(Conversazione, id=ticket_id)       
        tickets=Conversazione.objects.filter(reply=ticket)        
        serializer_data= TicketListSerializers(instance=tickets,many=True)
        return Response(data= serializer_data.data)


class DoneTicketView(LoginRequiredMixin,generics.UpdateAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Conversazione.objects.all()
    serializer_class = TicketUpdateSerializers
    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == "current":
            return self.request.user
        return super(DoneTicketView, self).get_object()
# _________________________________________________________________________________________________________________


class ChatCreateView(LoginRequiredMixin,APIView):
    def post(self,request):
        pm=Conversazione.objects.filter((Q(from_user=request.user) | Q(to_user=request.user)) , Q(is_reply = False ),(Q(state__contains={'status':'chat'})))
        ser_data=ChatCreateSerializers(data=request.data) 
        print(pm)
        if ser_data.is_valid():
            for p in pm :
                print(p.to_user)
                print(p.state)                      
                if p.to_user==ser_data.validated_data.get('to_user') or p.from_user==ser_data.validated_data.get('to_user'):
                    if p.state['block']==True:
                        return Response({"MSG": "block"}) 
                    return Response({"MSG": "این گفتگو وجود دارد"})                                                  
            ser_data.create(ser_data.validated_data,request)
            Meta.objects.create(user=request.user,meta_key='chat',meta_value=ser_data.data)  
            return Response(ser_data.data,status=status.HTTP_200_OK)            
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
                    
def handle_uploaded_file(f):
        with open(f.name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)


class SendMessageView(LoginRequiredMixin,APIView):
    def get(self,request,chat_id):
        chat = get_object_or_404(Conversazione, id=chat_id)
        if chat.state["delete"]==False:
            messeage=Conversazione.objects.filter(reply=chat)
            print(messeage)
            for pm in messeage:
                pm.state['is_read']=True
                pm.save()
            serializer_data= SendMessageSerializers(instance=messeage,many=True)
            return Response(data= serializer_data.data)
        return Response({"MSG": "این گفتگو وجود ندارد"})
    
    def post(self,request,chat_id,*args,**kwargs):        
        chat=get_object_or_404(Conversazione,id=chat_id)       
        ser_data=SendMessageSerializers(data=request.data)  
        print(request.session)
        if ser_data.is_valid():
            attachments = ser_data.validated_data.get('attachments')
            message=ser_data.validated_data.get('message')
            print('--------------------------')
            print(attachments)
           
            if chat.state["active"]==True  :          
                if request.user != chat.to_user :
                    ser_data.save(from_user=request.user,to_user=chat.to_user ,reply = chat,is_reply = True,state={'is_read':False})
                    
                else:
                    ser_data.save(from_user=request.user ,to_user=chat.from_user ,reply = chat,is_reply = True,state={'is_read':False})
                    Meta.objects.create(user=request.user,meta_key='chat',meta_value=ser_data.data) 
                # file_list=[]
                # for item in attachments:
                #     # attachments.append(item)
                #     file_list.append(item)
                # if file_list:
                #     attachments=file_list
            
                # if 'attachments' not in request.FILES or not ser_data.is_valid():
                #     return Response(status=status.HTTP_400_BAD_REQUEST)
                # else:
                #     handle_uploaded_file(request.FILES.getlist['attachments'])
            
                
                if message:  
                    chat.last_pm=message
                elif attachments:
                    chat.last_pm=attachments
                chat.save()
                if ser_data.data['message'] and ser_data.data['attachments']: 
                    return Response(ser_data.data,status=status.HTTP_200_OK)
                elif ser_data.data['message']:
                    return Response(ser_data.data['message'],status=status.HTTP_200_OK)  
                elif ser_data.data['attachments']:
                    return Response(ser_data.data['attachments'],status=status.HTTP_200_OK)
               
            else:
                return Response({"MSG": "این گفتگو فعال نیست"})
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)

# class FileView(APIView):
#     def post(self,request,chat_id):
#         ser_data= MultipleFileSerializers(data=request.data or None)
#         ser_data.is_valid(raise_exception=True)
#         attachments=ser_data.validated_data.get(attachments)

#         files_list=[]
#         for file in attachments:
#             files_list.append(Conversazione(attachments=attachments))

#         if files_list:
#             Conversazione.objects.bulk_create(files_list)
#         return Response(ser_data.data,status=status.HTTP_200_OK)  


class ListConversazioneView(LoginRequiredMixin,APIView):
    def get(self,request,pk):     
        user = get_object_or_404(User, pk=pk)   
        pm=Conversazione.objects.filter((Q(from_user=request.user) | Q(to_user=request.user)) , Q(is_reply = False ),(Q(state__contains={'delete': False})))
        print(pm)
        if user == request.user:
            serializer_data= ListConversazioneSerializers(instance=pm,many=True)
        else:
            return Response({'permission_denied' : "شما اجازه ی مشاهده ندارید"})
        return Response(data= serializer_data.data)


class DeleteConversazioneView(LoginRequiredMixin,APIView):
    def post(selt,request,pk=None):
        message=get_object_or_404(Conversazione,pk=pk)
        if message.to_user==request.user or message.from_user == request.user:
            print(request.user  )
            if message.state['delete']==False:
                message.state['delete']=True
                message.state['active']=False
                message.state['description_delete']={'user':request.user.id,'datetime':str(datetime.now())}
                message.save()
                return Response({"MSG": "گفتگو حذف شد"})
            return Response({"MSG": "این گفتگو وجود ندارد"})
        return Response({'permission_denied' : "شما اجازه ی حذف این گفتگو را  ندارید"})



class BlockConversazioneView(LoginRequiredMixin,APIView):
    def post(selt,request,pk=None):
        message=get_object_or_404(Conversazione,pk=pk)
        if message.to_user==request.user or message.from_user == request.user:
            message.state['block']=True
            message.state['active']=False
            message.state['description_block']={'user':request.user.id,'datetime':str(datetime.now())}
            message.save()
            return Response({"MSG": "کاربر بلاک شد"})
        return Response({'permission_denied' : "شما اجازه ی بلاک کردن ندارید"})

class UnBlockConversazioneView(LoginRequiredMixin,APIView):
    def post(selt,request,pk=None):
        message=get_object_or_404(Conversazione,pk=pk)
        if message.to_user==request.user or message.from_user == request.user:
            if message.state['block']==True and message.state['description_block']['user']==request.user.id:
                message.state['active']=True
                message.state['block']=False
                message.save()
                return Response({"MSG": "کاربر آنبلاک شد"})
        return Response({'permission_denied' : "شما اجازه ی آنبلاک کردن ندارید"})

#_____________________________________________________________________________________________________________________

class ChannelCreateView(LoginRequiredMixin,APIView):
    def post(self, request):
        ser_data=ChannelCreateSerializers(data=request.data)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data,request)
            return Response(ser_data.data,status=status.HTTP_200_OK)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)


class SendMessageChannelView(LoginRequiredMixin,APIView):
    def get(self,request,channel_id):
        channel = get_object_or_404(Channel, id=channel_id)
        message=Message.objects.filter(channel=channel)
        print(message)
        for pm in message:
            pm.state['is_read']=True
            pm.save()
        serializer_data= MessageCreateSerializers(instance=message,many=True)
        return Response(data= serializer_data.data)
        
    def post(self,request,channel_id):        
        channel=get_object_or_404(Channel,id=channel_id,members__id=request.user.id)       
        ser_data=MessageCreateSerializers(data=request.data)  
        if ser_data.is_valid():
            if request.user == channel.admin and channel.state['is_group']==False  :
                attachments = ser_data.validated_data.get('attachments')
                message=ser_data.validated_data.get('message')
                ser_data.save(from_user=channel.admin ,channel=channel,message=message,attachments=attachments)
            elif request.user != channel.admin and channel.state['is_group']==True:
                attachments = ser_data.validated_data.get('attachments')
                message=ser_data.validated_data.get('message')
                ser_data.save(from_user=request.user,channel=channel,message=message,attachments=attachments)
            else:
                return Response({'permission_denied' : "شما اجازه ی فرستادن پیام را  ندارید"})
            if message:  
                channel.last_pm=message
            elif attachments:
                channel.last_pm=attachments
            channel.save()
            if ser_data.data['message'] and ser_data.data['attachments']: 
                return Response(ser_data.data,status=status.HTTP_200_OK)
            elif ser_data.data['message']:
                return Response(ser_data.data['message'],status=status.HTTP_200_OK)  
            elif ser_data.data['attachments']:
                return Response(ser_data.data['attachments'],status=status.HTTP_200_OK)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)


class ListChannelView(LoginRequiredMixin,APIView):
    def get(self,request,pk):     
        user = get_object_or_404(User, pk=pk)   
        pm=Channel.objects.filter(Q(members__id=str(user.id)),(Q(state__contains={'delete': False})))
        print(pm)
        if user == request.user:
            serializer_data= ListChannelSerializers(instance=pm,many=True)
        else:
            return Response({'permission_denied' : "شما اجازه ی مشاهده ندارید"})
        return Response(data= serializer_data.data)

class DeleteChannelView(LoginRequiredMixin,APIView):
    def post(selt,request,pk=None):
        channel=get_object_or_404(Channel,pk=pk)
        if channel.admin==request.user:
            channel.state['delete']=True
            channel.state['description_delete']={'user':request.user.id,'datetime':str(datetime.now())}
            channel.save()
            return Response({"MSG": "گفتگو حذف شد"})
        return Response({'permission_denied' : "شما اجازه ی حذف این گفتگو را  ندارید"})

class JoinChannelView(APIView):
    def post(self,request,pk):
        channel=get_object_or_404(Channel,pk=pk)
        if channel.state['private']== False:
            channel.members.add(request.user) 
            channel.save()
            return Response({"MSG": " اضافه شدید"})
        else:
            return Response({'permission_denied' : " فقط ادمین اجازه ی اضافه کردن اعضا را دارد"})



class EditChannelView(LoginRequiredMixin,generics.UpdateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializers() 
    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == "current":
            return self.request.user
    def update(self, request, *args, **kwargs):
        # Partial update of the data
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)

class EditChannelView(LoginRequiredMixin,generics.UpdateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializers
    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == "current":
            return self.request.user
        return super(EditChannelView, self).get_object()
    

class RemoveMemberView(LoginRequiredMixin,generics.UpdateAPIView):
    queryset = Channel.objects.all()
    serializer_class = RemoveMemberSerializers
    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == "current":
            return self.request.user
        return super(RemoveMemberView, self).get_object()