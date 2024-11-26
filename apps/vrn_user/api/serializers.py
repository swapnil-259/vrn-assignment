from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.vrn_common.models import RoleUserMapping
from apps.vrn_user.models import Registration
from datetime import datetime,timezone
from apps.vrn_manager.models import Events

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['event']
    def __init__(self, *args, **kwargs):
        super(RegistrationSerializer, self).__init__(*args, **kwargs)
        for field in self.fields:
                self.fields[field].required = True
    def validate(self, attrs):
        event = attrs['event']

        if not self.context['request'].user.is_authenticated:
            raise ValidationError('You are not authenticated')
        if not RoleUserMapping.objects.filter(user=self.context['request'].user, role__parent='USER').exists():
            raise ValidationError('You are not authorized to register for events')

        if Registration.objects.filter(user=self.context['request'].user, event=event).exists():
            raise ValidationError('You are already registered for this event')
        event_start_date_naive = event.start_date.replace(tzinfo=None)
        now_naive = datetime.now().replace(tzinfo=None)
        if now_naive > event_start_date_naive:
            raise ValidationError('This event has already started')
        if event.capacity <= 0:
            raise ValidationError('This event has reached maximum capacity')
        event.capacity -= 1
        event.save()

        return attrs

    def create(self, validated_data):
        event = validated_data['event']
        event.save() 
        validated_data['user']=self.context['request'].user
        return Registration.objects.create(**validated_data)
    
class CancelRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['event'] 
    def __init__(self, *args, **kwargs):
        super(CancelRegistrationSerializer, self).__init__(*args, **kwargs)
        for field in self.fields:
                self.fields[field].required = True
    def validate(self, attrs):
        event = attrs['event']

        if not self.context['request'].user.is_authenticated:
            raise ValidationError('You are not authenticated')
        if not RoleUserMapping.objects.filter(user=self.context['request'].user, role__parent='USER').exists():
            raise ValidationError('You are not authorized to register for events')
        if not Events.objects.filter(id=event.pk).exists():
            raise serializers.ValidationError('Invalid event ID')
        event_start_date_naive = event.start_date.replace(tzinfo=None)
        now_naive = datetime.now().replace(tzinfo=None)
        if now_naive >= event_start_date_naive:
            raise serializers.ValidationError("Cannot cancel a registration for a started event")
        return attrs
    def update(self, instance, validated_data):
        instance.is_cancelled=True
        instance.event.capacity += 1
        instance.save()
        instance.event.save()

        return instance

