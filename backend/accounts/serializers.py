from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from core.models import MachineOwnershipInfo

User = get_user_model()

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Неверные учетные данные')
        attrs['user'] = user
        return attrs
    

class UserSerializer(serializers.ModelSerializer):
    service_companies = serializers.SerializerMethodField()

    def get_service_companies(self, obj):
        service_companies = set()
        for machine in MachineOwnershipInfo.objects.filter(client=obj):
            for company in machine.service_companies.all():
                service_companies.add(company.username)
        return list(service_companies)

    class Meta:
        model = User
        fields = ['username', 'last_name', 'is_client', 'is_service_company', 'service_companies']
