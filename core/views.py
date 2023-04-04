import core.models as models
import core.serializers as serializers
import core.permissions as permissions
from payment.models import PaymentGateway
from payment.serializers import PaymentGatewaySerializer
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import *
from rest_framework import permissions as rest_framework_permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.generic import TemplateView


class ApiRoot(APIView):
    name = 'api-root'
    BASE_REVERSE = "core:"

    def get(self, request, *args, **kwargs):
        data = {
            'clients': reverse(ApiRoot.BASE_REVERSE+ClientListCreateView.name, request=request),
            'address': reverse(ApiRoot.BASE_REVERSE+AddressListCreateView.name, request=request),
            'products': reverse(ApiRoot.BASE_REVERSE+ProductListView.name, request=request),
            'categories': reverse(ApiRoot.BASE_REVERSE+CategoryListView.name, request=request),
            "status": reverse(ApiRoot.BASE_REVERSE+StatusListView.name, request=request),
            "checkouts": reverse(ApiRoot.BASE_REVERSE+CheckoutListCreateView.name, request=request),
            "checkoutitems": reverse(ApiRoot.BASE_REVERSE+CheckoutItemCreateView.name, request=request),
            "paymentmethods": reverse(ApiRoot.BASE_REVERSE+PaymentMethodListView.name, request=request),
            "paymentgateways": reverse(ApiRoot.BASE_REVERSE+PaymentGatewayListView.name, request=request),
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
    name = 'category-list-view'
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


class StatusListView(ListAPIView):
    name = 'status-list-view'
    queryset = models.Status.objects.get_queryset()
    serializer_class = serializers.StatusSerializer
    permission_classes = [rest_framework_permissions.IsAuthenticated, permissions.ReadOnlyPermission]


class StatusDetail(RetrieveAPIView):
    name = 'status-detail'
    queryset = models.Status.objects.get_queryset()
    serializer_class = serializers.StatusDetailSerializer
    permission_classes = [rest_framework_permissions.IsAuthenticated]


class CheckoutListCreateView(ListCreateAPIView):
    name = 'checkout-list-create-view'
    queryset = models.Checkout.objects.get_queryset()
    serializer_class = serializers.CheckoutSerializer
    permission_classes = []

    def list(self, request, *args, **kwargs):
        current_user = request.user
        checkouts = models.Checkout.objects.filter(customer=current_user.id)
        serializer_checkout = serializers.CheckoutDetailSerializer(checkouts, many=True)
        return Response(serializer_checkout.data, status=status.HTTP_200_OK)


class CheckoutDetail(RetrieveAPIView):
    name = 'checkout-detail'
    queryset = models.Checkout.objects.get_queryset()
    serializer_class = serializers.CheckoutDetailSerializer
    permission_classes = [permissions.IsCheckoutOwner]


class CheckoutItemCreateView(CreateAPIView):
    name = 'checkou-item-create-view'
    queryset = models.CheckoutItem.objects.get_queryset()
    serializer_class = serializers.CheckoutItemSerializer
    permission_classes = []


class CheckoutItemDetail(RetrieveAPIView):
    name = 'checkout-item-detail'
    queryset = models.CheckoutItem.objects.get_queryset()
    serializer_class = serializers.CheckoutItemSerializer
    permission_classes = [rest_framework_permissions.IsAuthenticated, permissions.IsCheckoutItemOwner]


class PaymentMethodListView(ListAPIView):
    name = 'payment-method-list-view'
    queryset = models.PaymentMethod.objects.get_queryset()
    serializer_class = serializers.PaymentMethodSerializer
    permission_classes = [rest_framework_permissions.IsAuthenticated]


class PaymentGatewayListView(ListAPIView):
    name = 'payment-gateway-list-view'
    queryset = PaymentGateway.objects.get_queryset()
    serializer_class = PaymentGatewaySerializer
    permission_classes = [rest_framework_permissions.IsAuthenticated]


class SuccessView(TemplateView):
    template_name = "products/success.html"


class CancelView(TemplateView):
    template_name = "products/cancel.html"
