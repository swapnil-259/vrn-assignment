from apps.vrn_common.models import RoleUserMapping
from rest_framework.views import APIView
from apps.vrn_manager.api.serializers import EventSerializer
from apps.vrn_manager.models import Organization,Events
from rest_framework.response import Response
from rest_framework import status
from apps.vrn_user.models import Registration
from common.constants import status_message
class AllOrganizationView(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            if RoleUserMapping.objects.filter(role__parent__in =['USER' ,'ADMIN'], user = request.user).exists():
                org = list(Organization.objects.filter(deleted_status=False).values('user__first_name','user__email','name','description','address','phone_number'))
                return Response(org)
            else:
                return Response({'msg':status_message.NOT_AUTHORIZED},status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'msg':status_message.NOT_AUTHENTICATED},status = status.HTTP_401_UNAUTHORIZED)
            
                
class EventOrganizationWise(APIView):
    def get(self,request,pk):
        if request.user.is_authenticated:
            if RoleUserMapping.objects.filter(role__parent__in =['USER' ,'ADMIN'],user = request.user).exists():
                org = Organization.objects.filter(id = pk).first()
                if org is None:
                    return Response({'msg':'Organization not exist'},status=status.HTTP_400_BAD_REQUEST)
                events = Events.objects.filter(org=org) 
                serializer = EventSerializer(events,many=True)
                return Response(serializer.data)
            else:
                return Response({'msg':status_message.NOT_AUTHORIZED},status = status.HTTP_403_FORBIDDEN)
        else:
                return Response({'msg':status_message.NOT_AUTHENTICATED},status = status.HTTP_401_UNAUTHORIZED)
        

class EventDetailsView(APIView):
    def get(self,request,pk):
        if request.user.is_authenticated:
            if RoleUserMapping.objects.filter(role__parent__in=['MANAGER','USER','ADMIN'],user = request.user).exists():
                event = Events.objects.filter(id = pk)
                serializer = EventSerializer(event,many=True)
                return Response(serializer.data)
            else:
                return Response({'msg':status_message.NOT_AUTHORIZED},status = status.HTTP_403_FORBIDDEN)
        else:
                return Response({'msg':status_message.NOT_AUTHENTICATED},status = status.HTTP_401_UNAUTHORIZED)
        
class GetAllRegistrationsView(APIView):
    def get(self, request,pk):
        if request.user.is_authenticated:
            if RoleUserMapping.objects.filter(role__parent__in=['MANAGER', 'ADMIN'], user=request.user).exists():
                registrations = list(Registration.objects.filter(is_cancelled=False,event = pk).values(
                    'user__email',
                    'user__first_name',
                ))
                data = {
                    "registration_count":len(registrations),
                    "data":registrations
                }
                return Response(data)
            else:
                return Response({'msg':status_message.NOT_AUTHORIZED},status = status.HTTP_403_FORBIDDEN)
        else:
            return Response({'msg':status_message.NOT_AUTHENTICATED}, status=status.HTTP_401_UNAUTHORIZED)    