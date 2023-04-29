from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, CreateAPIView
from checkout import models, serializers
import checkout.permissions as custom_permissions


class ApiRoot(APIView):
    name = 'api-root'
    BASE_REVERSE = "checkout:"

    def get(self, request, *args, **kwargs):
        data = {
            "status": reverse(ApiRoot.BASE_REVERSE+StatusListView.name, request=request),
            "checkouts": reverse(ApiRoot.BASE_REVERSE+CheckoutListCreateView.name, request=request),
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
    
    def get(self, request, *args, **kwargs):
        status = models.Status.objects.filter(id=kwargs['pk'])
        print(status)
        status_serializer = serializers.StatusDetailSerializer(status, many=True)
        print(status_serializer.data)
        return Response(status_serializer.data[0])  


class CheckoutListCreateView(ListCreateAPIView):
    name = 'checkout-list-create-view'
    queryset = models.Checkout.objects.get_queryset()
    serializer_class = serializers.CheckoutSerializer
    permission_classes = [custom_permissions.IsAuthenticated] 

class CheckoutDetail(RetrieveAPIView):
    name = 'checkout-detail'
    queryset = models.Checkout.objects.get_queryset()
    serializer_class = serializers.CheckoutDetailSerializer
    permission_classes = [custom_permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        checkout = models.Checkout.objects.filter(customer=kwargs['pk'])
        checkout_serializer = serializers.CheckoutDetailSerializer(checkout, many=True)
        return Response(checkout_serializer.data, status=status.HTTP_200_OK)
        

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
