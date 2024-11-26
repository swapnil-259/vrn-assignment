from rest_framework import serializers
from apps.vrn_manager.models import Events,Organization

class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=-True)
    class Meta:
        model = Events
        fields = ['id','name','description','start_date','end_date','location','capacity']
    def __init__(self, *args, **kwargs):
        super(EventSerializer, self).__init__(*args,**kwargs)
        for field in self.fields:
                self.fields[field].required = True
    def create(self, validated_data):
        validated_data['org']=Organization.objects.get(user = self.context['request'].user)
        event = Events.objects.create(**validated_data)
        return event 
    