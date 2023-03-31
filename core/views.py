from django.shortcuts import render
from .models import Customer
from .serializers import *
from .permissions import *

from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import *
from rest_framework import permissions as rest_framework_permissions
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
class ApiRoot(APIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        data = {
            'clients': reverse(ClientListCreateView.name, request= request),
            'address': reverse(AddressListCreateView.name, request=request)
        }
        return Response(data, status=status.HTTP_200_OK)
    
class ClientListCreateView(CreateAPIView):
    name = 'client-list-create-view'
    queryset = Customer.objects.get_queryset()
    serializer_class = ClientSerializer

class ClientDetailUpdate(RetrieveUpdateAPIView):
    name = 'client-detail-update'
    queryset = Customer.objects.get_queryset()
    serializer_class = ClientSerializer
    permission_classes = [rest_framework_permissions.IsAuthenticated, IsClientOwner]

class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class AddressListCreateView(ListCreateAPIView):
    name = 'address-list-create-view'
    queryset = Address.objects.get_queryset()
    serializer_class = AddressSerializer

    def list(self, request, *args, **kwargs):
        current_user = request.user
        address = Address.objects.filter(customer=current_user.id)
        address_serializer = AddressSerializer(address, many=True)
        return Response(address_serializer.data, status.HTTP_200_OK)
    
class AddressDetailUpdateDestroy(RetrieveUpdateDestroyAPIView):
    name = 'address-detail-update-destroy'
    queryset = Address.objects.get_queryset()
    serializer_class  = AddressSerializer
    permission_classes = [rest_framework_permissions.IsAuthenticated, IsAddressOwnerDetail]
     
