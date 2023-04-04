import core.models as models
import core.serializers as serializers
import core.permissions as permissions
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import *
from rest_framework import permissions as rest_framework_permissions
from rest_framework_simplejwt.views import TokenObtainPairView


class ApiRoot(APIView):
    name = 'api-root'
    BASE_REVERSE = "core:"

    def get(self, request, *args, **kwargs):
        data = {
            'clients': reverse(ApiRoot.BASE_REVERSE+ClientListCreateView.name, request=request),
            'address': reverse(ApiRoot.BASE_REVERSE+AddressListCreateView.name, request=request),
            'products': reverse(ApiRoot.BASE_REVERSE+ProductListView.name, request=request),
            'categories': reverse(ApiRoot.BASE_REVERSE+CategoryListView.name, request=request)
        }
        return Response(data, status=status.HTTP_200_OK)


class ClientListCreateView(CreateAPIView):
    name = 'client-list-create-view'
    queryset = models.Customer.objects.get_queryset()
    serializer_class = serializers.ClientSerializer


class ClientDetailUpdate(RetrieveUpdateAPIView):
    name = 'client-detail-update'
    queryset = models.Customer.objects.get_queryset()
    serializer_class = serializers.ClientSerializer
    permission_classes = [rest_framework_permissions.IsAuthenticated, permissions.IsClientOwner]


class TokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.TokenObtainPairSerializer


class AddressListCreateView(ListCreateAPIView):
    name = 'address-list-create-view'
    queryset = models.Address.objects.get_queryset()
    serializer_class = serializers.AddressSerializer

    def list(self, request, *args, **kwargs):
        current_user = request.user
        address = models.Address.objects.filter(customer=current_user.id)
        address_serializer = serializers.AddressSerializer(address, many=True)
        return Response(address_serializer.data, status.HTTP_200_OK)


class AddressDetailUpdateDestroy(RetrieveUpdateDestroyAPIView):
    name = 'address-detail-update-destroy'
    queryset = models.Address.objects.get_queryset()
    serializer_class = serializers.AddressSerializer
    permission_classes = [rest_framework_permissions.IsAuthenticated, permissions.IsAddressOwnerDetail]


class CategoryListView(ListAPIView):
    name = 'category=list-view'
    queryset = models.Category.objects.get_queryset()
    serializer_class = serializers.CategorySerializer


class CategoryDetail(RetrieveAPIView):
    name = 'category-detail'
    queryset = models.Category.objects.get_queryset()
    serializer_class = serializers.CategorySerializer


class ProductListView(ListAPIView):
    name = 'product-list-view'
    queryset = models.Product.objects.get_queryset()
    serializer_class = serializers.ProductSerializer


class ProductDetail(RetrieveAPIView):
    name = 'product-detail'
    queryset = models.Product.objects.get_queryset()
    serializer_class = serializers.ProductSerializer
