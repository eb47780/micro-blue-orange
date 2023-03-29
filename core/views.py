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
            'clients': reverse(ClientListView.name, request= request)
        }
        return Response(data, status=status.HTTP_200_OK)
    
class ClientListView(CreateAPIView):
    name = 'client-list'
    queryset = Customer.objects.get_queryset()
    serializer_class = ClientSerializer

class ClientDetail(RetrieveUpdateAPIView):
    name = 'client-detail'
    queryset = Customer.objects.get_queryset()
    serializer_class = ClientSerializer
    permission_classes = [rest_framework_permissions.IsAuthenticated, IsClientOwner]

class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer