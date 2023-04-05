from django.urls import path
from .views import *

app_name = 'prductcore'


urlpatterns = [
    # Root API
    path('', ApiRoot.as_view(), name=ApiRoot.name),

    # api products
    path('api/products/v1', ProductListView.as_view(), name=ProductListView.name),
    path('api/product/<str:pk>', ProductDetail.as_view(), name=ProductDetail.name),

    # api categories
    path('api/categories/v1', CategoryListView.as_view(), name=CategoryListView.name),
    path('api/category/<str:pk>', CategoryDetail.as_view(), name=CategoryDetail.name),
]
