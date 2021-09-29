from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Project,ProjectTradie


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectUpdateSerializer(serializers.ModelSerializer):
    project_id = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=50)
    contact_details = serializers.CharField(max_length=20,)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    plans = serializers.CharField(max_length=20)
    status = serializers.CharField(max_length=50,default="Planned")
    file = serializers.FileField()

    class Meta:
        model = Project
        fields = ('project_id', 'address', 'contact_details',
                  'email', 'phone', 'plans', 'status', 'file')


class ProjectCreateSerializer(serializers.ModelSerializer):
    project_id = serializers.CharField(required=True, max_length=50)
    address = serializers.CharField(max_length=50,required=True)
    contact_details = serializers.CharField(required=True, max_length=50)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=20,required=True)
    plans = serializers.CharField(max_length=20,)
    status = serializers.CharField(max_length=50,default="Planned")
    file = serializers.FileField()

    class Meta:
        model = Project
        fields = ('project_id', 'address', 'contact_details',
                  'email', 'phone', 'plans', 'status', 'file')


class ProjectTradieSerializer(serializers.ModelSerializer):
    project_id = serializers.CharField(required=True, max_length=50)
    tradie_id = serializers.CharField(required=True, max_length=50)
    
    class Meta:
        model = ProjectTradie
        fields = ('project_id', 'tradie_id')
