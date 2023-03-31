# Models
from .models import *
from authcore.models import UserClient

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Client serializer
class ClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(source='authcore.user.password', write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'password', 'phone']

    def create(self, validated_data):
        if Customer.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({"detail": "User email already exists"})
        user_data = validated_data.pop('authcore')['user']
        user_data['username'] = validated_data['name']
        user_data['email'] = validated_data['email']
        user_client = UserClient.objects.create_client(**user_data)
        customer = Customer.objects.create(id = user_client.id, user = user_client, **validated_data)
        return customer
    
# Token obtainer
class TokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['id'] = self.user.id
        data['username'] = self.user.username
        data['email'] = self.user.email
        return data
    
# Address Serializers
class AddressSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(write_only=True)
    
    class Meta:
        model = Address
        fields = ['id', 'customer', 'street', 'street_number', 'city', 'zipcode']
        read_only_fields = ['customer']

    def create(self, validated_data):
        user_id = validated_data.pop('customer')
        if Address.objects.filter(customer=user_id).exists():
            raise serializers.ValidationError({'detail': 'Address already exists'})
        customer = Customer.objects.get(id=user_id)
        return Address.objects.create(customer=customer, **validated_data)
    
    def update(self, instance, validated_data):
        user_id = validated_data.pop('customer')
        if not Customer.objects.filter(id=user_id).exists():
            raise serializers.ValidationError({"detail": "No user found"})
        instance.street = validated_data.get('street', instance.street)
        instance.street_number = validated_data.get('street_number', instance.street_number)
        instance.city = validated_data.get('city', instance.city)
        instance.zipcode = validated_data.get('zipcode', instance.zipcode)
        instance.save()
        return instance