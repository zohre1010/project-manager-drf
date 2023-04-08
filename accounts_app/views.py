
from rest_framework import viewsets, mixins,status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from accounts_app.models import OtpCode
from accounts_app.serializers import *
from django.contrib.auth import get_user_model
from rest_framework import generics,permissions
from .serializers import UserInfoserializers
from rest_framework.response import Response
from .models import User as Model_User
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import   logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .permissions import IsAdminOrReadOnly
from django.contrib.auth.mixins import LoginRequiredMixin
from meta.models import Meta
from django.db.models import Q
User = get_user_model()

def get_tokens_for_user(user):
    refresh=RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }

class OTPViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = OtpCode.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return SendOtpSerializer
        return VerifyOtpSerializer

    @action(detail=False, methods=['POST'], url_path='verify')
    def verify_otp(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class UserPasswordResetView(APIView):
    def post(self, request):             
        ser_data=SendOtpSerializer(data=request.data)    
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data,status=status.HTTP_200_OK)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetConfirmView(APIView):
    def post(self, request):
        ser_data=VerifyOtpForPasswordSerializer(data=request.data)    
        if ser_data.is_valid():
            return Response(ser_data.data,status=status.HTTP_200_OK)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)

class ForgetPasswordView(APIView): 
    permission_classes = (IsAdminOrReadOnly,)
    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        serializer = ForgetPasswordSerializer(user, data=request.data)
        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserInfoserializers

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == "current":
            return self.request.user
        
        return super(UserProfileUpdateView, self).get_object()


 
class UserDeleteView(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset=Model_User.objects.all()
    def delete(selt,request,pk=None):
        users=get_object_or_404(selt.queryset,pk=pk)
        if users != request.user.is_admin:
            return Response({'permission_denied' : 'شما ادمین نیستید'})
        users.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


@api_view(['GET'])
def current_user(request):
    user = request.user    
    if user.phone_number : 
        return Response({'email': user.phone_number})
    else:
        return Response({'msg': 'no user'})
    

class LogoutView(LoginRequiredMixin,APIView):
    def post(self, request, format=None):        
        if request.user.full_name:
            meta=Meta.objects.create(user=request.user,meta_key='logout',meta_value=request.user.full_name)
            Meta.objects.create(user=request.user,meta_key='offline',meta_value=request.user.full_name)
        else:
            meta=Meta.objects.create(user=request.user,meta_key='logout',meta_value=request.user.phone_number)
            Meta.objects.create(user=request.user,meta_key='offline',meta_value=request.user.phone_number)
        logout(request)
        return Response({"MSG": "شما خارج شدید"}, status=status.HTTP_200_OK)


class LoginView(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        data = request.POST        
        phone_number = data.get('phone_number')
        password = data.get('password')
        user = authenticate(request,phone_number=phone_number, password=password)    
     

        if user is not None:           
            login(request, user)
            if user.full_name:
                meta=Meta.objects.create(user=request.user,meta_key='login',meta_value=user.full_name)
                Meta.objects.create(user=request.user,meta_key='online',meta_value=user.full_name)
            else:
                meta=Meta.objects.create(user=request.user,meta_key='login',meta_value=user.phone_number)
                Meta.objects.create(user=request.user,meta_key='online',meta_value=user.phone_number)
            return Response({'msg': ' وارد شدید'},status=status.HTTP_200_OK)            
        else:
            return Response({'msg': ' وارد شوید'},status=status.HTTP_404_NOT_FOUND)


class UserProfileView(LoginRequiredMixin, APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user == request.user:
            serializer_data= UserProfileSerializer(user)
            return Response(data= serializer_data.data)
        else:
            return Response({'permission_denied' : 'شما صاحب اکانت نیستید'})
        

class UserEditUpdateView(APIView):
    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        serializer = UserEditserializers(user, data=request.data, partial=True)
        if serializer.is_valid():
            if kwargs['pk']==request.user.id:
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'permission_denied' : 'شما صاحب اکانت نیستید'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListOfAdminView(APIView):   
    paginate_by = 10 
    def get(selt,request):
        users=Model_User.objects.filter(is_admin=True)
        serializer_data= UserIsAdminSerializers(instance=users,many=True)
        return Response(data= serializer_data.data)

class ListOfManagerView(APIView):    
    paginate_by = 10
    def get(selt,request):
        users=Model_User.objects.filter(manager=True)
        serializer_data= UserIsManegerSerializers(instance=users,many=True)
        return Response(data= serializer_data.data)

class ListEmployeeView(APIView): 
    paginate_by = 10   
    def get(selt,request):
        users=Model_User.objects.filter(Q(manager=False),Q(is_admin=False))
        serializer_data= ListUserSerializer(instance=users,many=True)
        return Response(data= serializer_data.data)

class UserlistView(APIView):
    paginate_by = 10  
    # permission_classes = (permissions.IsAuthenticated,)
    def get(selt,request):
        users=Model_User.objects.all()
        serializer_data= ListUserSerializer(instance=users,many=True)
        return Response(data= serializer_data.data)

class UpToAdminView(generics.UpdateAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = IsAdminSerializers
    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == "current":
            return self.request.user
        return super(UpToAdminView, self).get_object()

class UpToManagerView(generics.UpdateAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = IsManagerSerializers
    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == "current":
            return self.request.user
        return super(UpToManagerView, self).get_object()

#______________________________________________________________________
class SetOnlineView(APIView):
    def post(selt,request,pk=None):
        user=get_object_or_404(User,pk=pk)
        ser_data=OnlineSerializers(data=request.data)
        if ser_data.is_valid():
            if user==request.user:
                ser_data.create(ser_data.validated_data,request)
            else:
                return Response({'permission_denied' : 'شما صاحب اکانت نیستید'})
           
            return Response(ser_data.data,status=status.HTTP_200_OK)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)

class SetOfflineView(APIView):
    def post(selt,request,pk=None):
        user=get_object_or_404(User,pk=pk)
        ser_data=OfflineSerializers(data=request.data)
        if ser_data.is_valid():
            if user==request.user:
                ser_data.create(ser_data.validated_data,request)
            else:
                return Response({'permission_denied' : 'شما صاحب اکانت نیستید'})
            return Response(ser_data.data,status=status.HTTP_200_OK)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
    

class GetOnlineOrOfflineView(APIView):
    def get(selt,request,pk):
        user=get_object_or_404(User,pk=pk)
        meta=Meta.objects.filter(Q(user=user) , Q(meta_key='online')| Q(meta_key='offline')) 
        print(meta)
        print(meta.latest().meta_key)
        if meta.latest().meta_key=='online':
            return Response({'Msg':'online'})
        if meta.latest().meta_key=='offline':
            return Response({'Msg':'offline'})
        return Response({'Error' : 'oops'})

