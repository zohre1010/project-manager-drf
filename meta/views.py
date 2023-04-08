from django.shortcuts import render
from  rest_framework.views import APIView
from .serializers import *
from accounts_app.permissions import IsAdminOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Meta
from django.db.models import Q
# Create your views here.

class CreateNotifView(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def post(self,request):
        ser_data=NotifSerializers(data=request.data)
        print(ser_data.is_valid())
        if ser_data.is_valid():  
            ser_data.create(ser_data.validated_data,request)         
            return Response(ser_data.data,status=status.HTTP_200_OK)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)

class LastNotifView(APIView):
    def get(self,request):
        notif = Meta.objects.filter(meta_key='notif').latest()     
        serializer_data= NotifSerializers(instance=notif)
        return Response(serializer_data.data)


class NotifsView(APIView):
    def get(self,request):
        notif = Meta.objects.filter(meta_key='notif')
        serializer_data= NotifSerializers(instance=notif,many=True)
        return Response(serializer_data.data)


class ReportsView(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self,request):
        report = Meta.objects.all()
        serializer_data= ReportSerializers(instance=report,many=True)
        return Response(serializer_data.data)

class ReportOneUserView(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self,request,pk):
        user=get_object_or_404(User,pk=pk)
        report = Meta.objects.filter(user=user)
        serializer_data= ReportSerializers(instance=report,many=True)
        return Response(serializer_data.data)
    
class ReportTicketView(APIView):
    def get(self,request):
        ticket = Meta.objects.filter(meta_key='ticket')
        serializer_data= NotifSerializers(instance=ticket,many=True)
        return Response(serializer_data.data)

class ReportChatView(APIView):
    def get(self,request):
        chat = Meta.objects.filter(meta_key='chat')
        serializer_data= NotifSerializers(instance=chat,many=True)
        return Response(serializer_data.data)

class ReportLoginView(APIView):
    def get(self,request):
        meta = Meta.objects.filter(Q(meta_key='login')|Q(meta_key='logout'))
        serializer_data= NotifSerializers(instance=meta,many=True)
        return Response(serializer_data.data)

