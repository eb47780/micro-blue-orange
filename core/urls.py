from django.urls import path, include
from .views import *
from rest_framework_simplejwt import views as jwt_views

app_name = 'core'


urlpatterns = [
    # Root API
    path('', ApiRoot.as_view(), name=ApiRoot.name),

    # api clients/authentication
    path('api/clients/v1', ClientListCreateView.as_view(), name=ClientListCreateView.name),
    path('api/client/<str:pk>', ClientDetailUpdate.as_view(), name=ClientDetailUpdate.name),
    path('api/authentication', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # api client address
    path('api/address/v1', AddressListCreateView.as_view(), name=AddressListCreateView.name),
    path('api/address/<str:pk>', AddressDetailUpdateDestroy.as_view(), name=AddressDetailUpdateDestroy.name),

    # api products
    path('api/products/v1', ProductListView.as_view(), name=ProductListView.name),
    path('api/product/<str:pk>', ProductDetail.as_view(), name=ProductDetail.name),

    # api categories
    path('api/categories/v1', CategoryListView.as_view(), name=CategoryListView.name),
    path('api/category/<str:pk>', CategoryDetail.as_view(), name=CategoryDetail.name),

    # api payment
    path('api/checkouts/v1', CheckoutListCreateView.as_view(), name=CheckoutListCreateView.name),
    path('api/checkout/<str:pk>', CheckoutDetail.as_view(), name=CheckoutDetail.name),
    path('api/checkoutitems/v1', CheckoutItemCreateView.as_view(), name=CheckoutItemCreateView.name),
    path('api/checkoutitem/<str:pk>', CheckoutItemDetail.as_view(), name=CheckoutItemDetail.name),
    path('api/paymentmethods', PaymentMethodListView.as_view(), name=PaymentMethodListView.name),
    path('api/paymentgateways', PaymentGatewayListView.as_view(), name=PaymentGatewayListView.name),
]
