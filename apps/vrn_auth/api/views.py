from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.vrn_auth.api.serializers import RegisterUserSerializer,RegisterManagerSerializer,OrganizationSerializer
from apps.vrn_common.models import RoleUserMapping
from apps.vrn_manager.models import Organization
from common.constants import status_message
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class RegisterUser(APIView):
    def post(self,request):
        serializer = RegisterUserSerializer(data=request.data)
        if User.objects.filter(email=request.data.get("email")).exists():
            return Response(
                {"msg": status_message.EMAIL_ALREADY_REGISTERED},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data={}
        if serializer.is_valid():
            user = serializer.save()
            data["user"]=user.email
            refresh = RefreshToken.for_user(user)
            data['token'] =  {
                                'refresh':str(refresh),
                                'access':str(refresh.access_token),        
            } 
            return Response(data)
        else:
            return Response(serializer.errors)
    def get(self,request):
        if request.user.is_authenticated:
            if RoleUserMapping.objects.filter(user= request.user,role__parent = 'USER').exists():
                serializer = RegisterUserSerializer(request.user)
                return Response(serializer.data)
            else:
                return Response({'msg':status_message.NOT_AUTHORIZED},status=status.HTTP_403_FORBIDDEN)

        else:
            return Response({'msg':status_message.NOT_AUTHENTICATED},status=status.HTTP_401_UNAUTHORIZED)
        
class RegisterManager(APIView):
    def post(self,request):
        serializer = RegisterManagerSerializer(data=request.data)
        if User.objects.filter(email=request.data.get("email")).exists():
            return Response(
                {"msg": status_message.EMAIL_ALREADY_REGISTERED},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data={}
        if serializer.is_valid():
            user = serializer.save()
            data["user"]=user.email
            refresh = RefreshToken.for_user(user)
            data['token'] =  {
                                'refresh':str(refresh),
                                'access':str(refresh.access_token),        
            } 
            return Response(data)
        else:
            return Response(serializer.errors)
    def get(self,request):
        if request.user.is_authenticated:
            if RoleUserMapping.objects.filter(user= request.user,role__parent = 'MANAGER').exists():
                organization = Organization.objects.get(user=request.user) 
                serializer = OrganizationSerializer(organization)
                data = {
                    "email":request.user.email,
                    "name":request.user.first_name,
                    "org_details":serializer.data
                }
                return Response(data)
            else:
                return Response({'msg':status_message.NOT_AUTHORIZED},status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'msg':status_message.NOT_AUTHENTICATED},status = status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
     def post(self, request):
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'msg':'Logout Successfully'})
     
class GetAllUsers(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            if RoleUserMapping.objects.filter(user = request.user,role__parent='ADMIN').exists():
                users = RoleUserMapping.objects.filter(role__parent='USER').values(
                    'user__email','user__first_name'
                )
                return Response(list(users))
            else:
                return Response({'msg':status_message.NOT_AUTHORIZED},status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'msg':status_message.NOT_AUTHENTICATED},status = status.HTTP_401_UNAUTHORIZED)


class GetAllManagers(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            if RoleUserMapping.objects.filter(user = request.user,role__parent='ADMIN').exists():
                managers = Organization.objects.filter(deleted_status = False).values(
                    "user__email","user__first_name","name","description","address","phone_number"
                )
                return Response(list(managers))
            else:
                return Response({'msg':status_message.NOT_AUTHORIZED},status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'msg':status_message.NOT_AUTHENTICATED},status = status.HTTP_401_UNAUTHORIZED)
