from django.contrib.auth.models import User
from rest_framework import serializers

from apps.vrn_common.models import Configuration,RoleUserMapping
from apps.vrn_manager.models import Organization

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email','password','first_name']
    def __init__(self, *args, **kwargs):
        super(RegisterUserSerializer, self).__init__(*args, **kwargs)
        for field in self.fields:
                self.fields[field].required = True
    def create(self, validated_data):
        validated_data["username"]=validated_data.get('email')
        user = User.objects.create_user(**validated_data)
        default_role = Configuration.objects.get(parent="USER")
        RoleUserMapping.objects.create(user=user, role=default_role)
        return user
    

class RegisterManagerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    organization_name =serializers.CharField()
    phone_number=serializers.CharField()
    address=serializers.CharField()
    description=serializers.CharField()
    class Meta:
        model = User
        fields = ['email','password','first_name','organization_name','phone_number','address','description']
    def __init__(self, *args, **kwargs):
        super(RegisterManagerSerializer, self).__init__(*args, **kwargs)
        for field in self.fields:
                self.fields[field].required = True
    def create(self, validated_data):
        validated_data["username"]=validated_data.get('email')
        organization_data = {
            'name': validated_data.pop('organization_name'),
            'phone_number': validated_data.pop('phone_number'),
            'address': validated_data.pop('address'),
            'description': validated_data.pop('description'),
        }
        user = User.objects.create_user(**validated_data)
        manager_role = Configuration.objects.get(parent="MANAGER")
        RoleUserMapping.objects.create(user=user, role=manager_role)
        organization_data['user']=user
        Organization.objects.create(**organization_data)
        return user

    


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name','phone_number','address','description']