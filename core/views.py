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

# A Base Api Root for faster purposes
class ApiRoot(APIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        data = {
            'clients': reverse(ClientListCreateView.name, request= request),
            'address': reverse(AddressListCreateView.name, request=request),
            'products': reverse(ProductListView.name, request=request),
            'cateogories': reverse(CategoryListView.name, request=request)
        }
        return Response(data, status=status.HTTP_200_OK)

# Client Controller    
class ClientListCreateView(CreateAPIView):
    name = 'client-list-create-view'
    queryset = Customer.objects.get_queryset()
    serializer_class = ClientSerializer

class ClientDetailUpdate(RetrieveUpdateAPIView):
    name = 'client-detail-update'
    queryset = Customer.objects.get_queryset()
    serializer_class = ClientSerializer
    permission_classes = [rest_framework_permissions.IsAuthenticated, IsClientOwner]

# Token Controller
class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

# Address Controller
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

# Category Controller
class CategoryListView(ListAPIView):
    name = 'category=list-view'
    queryset = Category.objects.get_queryset()
    serializer_class = CategorySerializer

class CategoryDetail(RetrieveAPIView):
    name = 'category-detail'
    queryset = Category.objects.get_queryset()
    serializer_class = CategorySerializer

# Product Controller
class ProductListView(ListAPIView):
    name = 'product-list-view'
    queryset = Product.objects.get_queryset()
    serializer_class = ProductSerializer

class ProductDetail(RetrieveAPIView):
    name = 'product-detail'
    queryset = Product.objects.get_queryset()
    serializer_class = ProductSerializer
     
