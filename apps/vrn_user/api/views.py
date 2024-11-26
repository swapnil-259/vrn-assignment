from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from apps.vrn_user.api.serializers import RegistrationSerializer,CancelRegistrationSerializer
from common.constants import status_message

class RegisterEventView(APIView):
    def post(self,request):
        serializer = RegistrationSerializer(data = request.data,context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':status_message.SUCCESSFULLY_REGISTERED})
        else:
            return Response(serializer.errors)

class CancelRegistrationView(APIView):
    def post(self, request, pk):
        serializer = CancelRegistrationSerializer( data={'event': pk},context = {"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': status_message.REGISTRATION_CANCELLED})
        else:
            return Response(serializer.errors)
            