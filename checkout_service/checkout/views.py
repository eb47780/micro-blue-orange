from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework import permissions
from checkout import models, serializers
import checkout.permissions as custom_permissions


class ApiRoot(APIView):
    name = 'api-root'
    BASE_REVERSE = "checkout:"

    def get(self, request, *args, **kwargs):
        data = {
            "status": reverse(ApiRoot.BASE_REVERSE+StatusListView.name, request=request),
            "checkouts": reverse(ApiRoot.BASE_REVERSE+CheckoutCreateView.name, request=request),
            "checkoutitems": reverse(ApiRoot.BASE_REVERSE+CheckoutItemCreateView.name, request=request),
        }
        return Response(data, status=status.HTTP_200_OK)


class StatusListView(ListAPIView):
    name = 'status-list-view'
    queryset = models.Status.objects.get_queryset()
    serializer_class = serializers.StatusSerializer
    permission_classes = [custom_permissions.IsAuthenticated]


class StatusDetail(RetrieveAPIView):
    name = 'status-detail'
    queryset = models.Status.objects.get_queryset()
    serializer_class = serializers.StatusDetailSerializer
    permission_classes = [custom_permissions.IsAuthenticated]


class CheckoutCreateView(CreateAPIView):
    name = 'checkout-create-view'
    queryset = models.Checkout.objects.get_queryset()
    serializer_class = serializers.CheckoutSerializer
    permission_classes = [custom_permissions.IsAuthenticated]


class CheckoutDetail(RetrieveAPIView):
    name = 'checkout-detail'
    queryset = models.Checkout.objects.get_queryset()
    serializer_class = serializers.CheckoutDetailSerializer
    permission_classes = [custom_permissions.IsAuthenticated]


class CheckoutItemCreateView(CreateAPIView):
    name = 'checkou-item-create-view'
    queryset = models.CheckoutItem.objects.get_queryset()
    serializer_class = serializers.CheckoutItemSerializer
    permission_classes = [custom_permissions.IsAuthenticated]


class CheckoutItemDetail(RetrieveAPIView):
    name = 'checkout-item-detail'
    queryset = models.CheckoutItem.objects.get_queryset()
    serializer_class = serializers.CheckoutItemSerializer
    permission_classes = [custom_permissions.IsAuthenticated]
