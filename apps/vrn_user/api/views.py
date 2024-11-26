from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.vrn_user.api.serializers import RegistrationSerializer,CancelRegistrationSerializer

class RegisterEventView(APIView):
    def post(self,request):
        serializer = RegistrationSerializer(data = request.data,context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'You are successfully registered for this event'})
        else:
            return Response(serializer.errors)

class CancelRegistrationView(APIView):
    def post(self, request, pk):
        serializer = CancelRegistrationSerializer( data={'event': pk},context = {"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration canceled successfully.'})
        else:
            return Response(serializer.errors)
            