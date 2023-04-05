from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from authcore import models, serializers
import authcore.permissions as custom_permissions


class ApiRoot(APIView):
    name = 'api-root'
    BASE_REVERSE = "authcore:"

    def get(self, request, *args, **kwargs):
        data = {
            'clients': reverse(ApiRoot.BASE_REVERSE+ClientListCreateView.name, request=request),
            'address': reverse(ApiRoot.BASE_REVERSE+AddressListCreateView.name, request=request),
            'checkoutuser': reverse(ApiRoot.BASE_REVERSE+CheckoutUserCreateView.name, request=request)
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
    permission_classes = [permissions.IsAuthenticated, custom_permissions.IsClientOwner]


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
    permission_classes = [permissions.IsAuthenticated, custom_permissions.IsAddressOwnerDetail]


class CheckoutUserCreateView(ListCreateAPIView):
    name = 'checkout-user-create-view'
    serializer_class = serializers.CheckoutUserSerializer
    queryset = models.CheckoutUser.objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated]
