from datetime import timedelta, datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from utils import send_otp_code
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts_app.models import OtpCode

from accounts_app.generate_otp import generate_code_opt
from rest_framework.fields import empty
from django.contrib.auth import authenticate,login
from .models import User as Model_User 
from rest_framework.serializers import ValidationError
from rest_framework.authtoken.models import Token

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer

from  meta.models import Meta



User = get_user_model()


class CustomTokenObtain(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['phone_number'] = user.phone_number
        token['full_name'] = user.full_name
        token['email'] = user.email
        return token



class SendOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = ('phone_number',)

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        otp = generate_code_opt()
        send_otp_code(phone_number, otp)
        validated_data['otp'] = otp
        return super().create(validated_data)



class VerifyOtpSerializer(serializers.Serializer):
    # Request
    phone_number = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True)

    # Response
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    new_user = serializers.BooleanField(read_only=True)
    def validate(self, data):
        phone_number = data.get('phone_number')
        otp = data.get('otp')

        if not OtpCode.objects.filter(
                phone_number=phone_number,
                otp=otp,
                created_at__gte=datetime.now() - timedelta(minutes=settings.OTP_EXPIRE_TIME)).exists():
            raise serializers.ValidationError('کد صحیح نیست')
        return data
    def create(self, validated_data):
        phone_number = validated_data.get('phone_number')
        user, created = User.objects.get_or_create(phone_number=phone_number,status={'is_phone_verified': True,'is_active':True})
        if not created:
            if not user.phone_number:
                created = True                
            if not user.status['is_phone_verified'] :
                user.status['is_phone_verified'] = True
                user.save()                    
        validated_data['new_user'] = created
        # generate JWT Token
        refresh = CustomTokenObtain.get_token(user)
        access = refresh.access_token
        validated_data['refresh'] = str(refresh)
        validated_data['access'] = str(access)
        return validated_data


class UserInfoserializers(serializers.ModelSerializer):
    user_type= serializers.CharField(required=False)
    status = serializers.JSONField(required=False, initial=dict)
    password = serializers.CharField(required=False, write_only=True,style={'input_type': 'password'})
    phone_number=serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name','status','user_type')
        extra_kwargs = {'password': {'write_only': True} }
       

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user
    
 
class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model_User
        fields = ['id','full_name', 'email','phone_number','password']
        read_only_field=['id',]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model_User
        fields = ('email', 'phone_number', 'full_name','user_type')
        read_only_field=['id',]

class UserEditserializers(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('avatar','email')

class UserIsAdminSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('full_name','phone_number','is_admin')

class IsAdminSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_admin',)

class IsManagerSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('manager',)
class UserIsManegerSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('full_name','phone_number','manager')

class VerifyOtpForPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True)
    def validate(self, data):
        phone_number = data.get('phone_number')
        otp = data.get('otp')

        if not OtpCode.objects.filter(
                phone_number=phone_number,
                otp=otp,
                created_at__gte=datetime.now() - timedelta(minutes=settings.OTP_EXPIRE_TIME)).exists():
            raise serializers.ValidationError('کد صحیح نیست')
        return data      
       
class ForgetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['password',]   
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user

class OnlineSerializers(serializers.ModelSerializer):
    meta_key= serializers.CharField(read_only=True)
    user= serializers.PrimaryKeyRelatedField(read_only=True) 
    created=serializers.DateTimeField(read_only=True)
    class Meta:
        model=Meta
        fields=('user','meta_key','meta_value','created')
    def create(self, validated_data,request):
        meta_value=validated_data.get('meta_value')
        meta=Meta.objects.create(user=request.user,meta_key='online',meta_value=meta_value,created=datetime.now())
        validated_data['meta'] = meta
        return validated_data

class OfflineSerializers(serializers.ModelSerializer):
    meta_key= serializers.CharField(read_only=True)
    user= serializers.PrimaryKeyRelatedField(read_only=True) 
    created=serializers.DateTimeField(read_only=True)
    class Meta:
        model=Meta
        fields=('user','meta_key','meta_value','created')
    def create(self, validated_data,request):
        meta_value=validated_data.get('meta_value')
        meta=Meta.objects.create(user=request.user,meta_key='offline',meta_value=meta_value,created=datetime.now())
        validated_data['meta'] = meta
        return validated_data