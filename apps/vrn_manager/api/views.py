from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from apps.vrn_common.models import RoleUserMapping
from rest_framework.response import Response
from rest_framework import status
from apps.vrn_manager.api.serializers import EventSerializer
from apps.vrn_manager.models import Organization,Events
from datetime import date
class EventRegisterView(APIView):
    def post(self,request):
        if request.user.is_authenticated:
            if RoleUserMapping.objects.filter(role__parent='MANAGER',user = request.user).exists():
                serializer = EventSerializer(data=request.data, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg':'event registered successfully'})
                else:
                    return Response(serializer.errors)
            else:
                return Response({'msg':'you are not authorized'},status = status.HTTP_403_FORBIDDEN)
        else:
                return Response({'msg':'you are not authenticated'},status = status.HTTP_401_UNAUTHORIZED)
        
    def get(self,request):
        if request.user.is_authenticated:
            if RoleUserMapping.objects.filter(role__parent='MANAGER',user = request.user).exists():
                org = Organization.objects.get(user = request.user)
                print(org)
                events = Events.objects.filter(org=org) 
                serializer = EventSerializer(events,many=True)
                print(serializer.data)
                return Response(serializer.data)
            else:
                return Response({'msg':'you are not authorized'},status = status.HTTP_403_FORBIDDEN)
        else:
                return Response({'msg':'you are not authenticated'},status = status.HTTP_401_UNAUTHORIZED)
        

        

class CancelEvent(APIView):
    def post(self, request, pk):
        if request.user.is_authenticated:
            if RoleUserMapping.objects.filter(role__parent='MANAGER',user = request.user).exists():
                event = Events.objects.filter(id=pk,org__user = request.user).first()
                if event is None:
                    return Response({'message': 'Event not found.'}, status=status.HTTP_400_BAD_REQUEST)
                today = date.today()
                if event.start_date < today:
                    return Response({'message': 'Event has already started. Cannot cancel.'}, status=status.HTTP_400_BAD_REQUEST)
                else:    
                    event.is_cancelled = True
                    event.save()
                    return Response({'message': 'Event canceled successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg':'you are not authorized'},status = status.HTTP_403_FORBIDDEN)
        else:
                return Response({'msg':'you are not authenticated'},status = status.HTTP_401_UNAUTHORIZED)
        
        


