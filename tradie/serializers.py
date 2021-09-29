from rest_framework import serializers
from .models import Tradie

class TradieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tradie
        fields = '__all__'
        
class TradieUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    contact_details = serializers.CharField(max_length=20,)
    phone = serializers.CharField(max_length=20)
    active_plans = serializers.CharField(max_length=20)
    status = serializers.BooleanField(default=False)


    class Meta:
        model = Tradie
        fields = ('name','contact_details',
                  'email', 'phone', 'active_plans', 'status')
        
class TradieCreatreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    contact_details = serializers.CharField(max_length=20,)
    phone = serializers.CharField(max_length=20)
    active_plans = serializers.CharField(max_length=20)
    status = serializers.BooleanField(default=False)


    class Meta:
        model = Tradie
        fields = ('name','contact_details',
                  'email', 'phone', 'active_plans', 'status')