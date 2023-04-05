from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status
from productcore import models, serializers

class ApiRoot(APIView):
    name = 'api-root'
    BASE_REVERSE = "productcore:"

    def get(self, request, *args, **kwargs):
        data = {
            'products': reverse(ApiRoot.BASE_REVERSE+ProductListView.name, request=request),
            'categories': reverse(ApiRoot.BASE_REVERSE+CategoryListView.name, request=request),
        }
        return Response(data, status=status.HTTP_200_OK)

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
