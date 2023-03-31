import models
import serializers
import permissions
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions as rest_framework_permissions
from rest_framework_simplejwt.views import TokenObtainPairView


class ApiRoot(APIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        data = {
            'clients': reverse(ClientListCreateView.name, request=request),
            'address': reverse(AddressListCreateView.name, request=request),
            'products': reverse(ProductListView.name, request=request),
            'cateogories': reverse(CategoryListView.name, request=request)
        }
        return Response(data, status=status.HTTP_200_OK)


class ClientListCreateView(generics.CreateAPIView):
    name = 'client-list-create-view'
    queryset = models.Customer.objects.get_queryset()
    serializer_class = serializers.ClientSerializer


class ClientDetailUpdate(generics.RetrieveUpdateAPIView):
    name = 'client-detail-update'
    queryset = models.Customer.objects.get_queryset()
    serializer_class = serializers.ClientSerializer
    permission_classes = [rest_framework_permissions.IsAuthenticated, permissions.IsClientOwner]


class TokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.TokenObtainPairSerializer


class AddressListCreateView(generics.istCreateAPIView):
    name = 'address-list-create-view'
    queryset = models.Address.objects.get_queryset()
    serializer_class = serializers.AddressSerializer

    def list(self, request, *args, **kwargs):
        current_user = request.user
        address = models.Address.objects.filter(customer=current_user.id)
        address_serializer = serializers.AddressSerializer(address, many=True)
        return Response(address_serializer.data, status.HTTP_200_OK)


class AddressDetailUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    name = 'address-detail-update-destroy'
    queryset = models.Address.objects.get_queryset()
    serializer_class = serializers.AddressSerializer
    permission_classes = [rest_framework_permissions.IsAuthenticated, permissions.IsAddressOwnerDetail]


class CategoryListView(generics.ListAPIView):
    name = 'category=list-view'
    queryset = models.Category.objects.get_queryset()
    serializer_class = serializers.CategorySerializer


class CategoryDetail(generics.RetrieveAPIView):
    name = 'category-detail'
    queryset = models.Category.objects.get_queryset()
    serializer_class = serializers.CategorySerializer


class ProductListView(generics.ListAPIView):
    name = 'product-list-view'
    queryset = models.Product.objects.get_queryset()
    serializer_class = serializers.ProductSerializer


class ProductDetail(generics.RetrieveAPIView):
    name = 'product-detail'
    queryset = models.Product.objects.get_queryset()
    serializer_class = serializers.ProductSerializer
