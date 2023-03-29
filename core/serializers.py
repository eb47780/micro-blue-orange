from .models import *
from authcore.models import UserClient

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Create your serializers here.
class ClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(source='authcore.user.password', write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'password', 'phone']

    def create(self, validated_data):
        if Customer.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError("Validation Error: Email already exists")
        
        user_data = validated_data.pop('authcore')['user']
        user_data['username'] = validated_data['name']
        user_data['email'] = validated_data['email']
        user_client = UserClient.objects.create_client(**user_data)
        customer = Customer.objects.create(id = user_client.id, user = user_client, **validated_data)
        return customer
    
class TokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['id'] = self.user.id
        data['username'] = self.user.username
        data['email'] = self.user.email
        return data