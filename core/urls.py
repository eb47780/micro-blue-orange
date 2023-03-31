from django.urls import path, include
import views
from rest_framework_simplejwt import views as jwt_views

app_name = 'core'

# Create your urls here.
urlpatterns = [
    # Root API
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),

    # api clients/authentication
    path('api/clients/v1', views.ClientListCreateView.as_view(), name=views.ClientListCreateView.name),
    path('api/client/<str:pk>', views.ClientDetailUpdate.as_view(), name=views.ClientDetailUpdate.name),
    path('api/authentication', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # api client address
    path('api/address/v1', views.AddressListCreateView.as_view(), name=views.AddressListCreateView.name),
    path('api/address/<str:pk>', views.AddressDetailUpdateDestroy.as_view(), name=views.AddressDetailUpdateDestroy.name),

    # api products
    path('api/products/v1', views.ProductListView.as_view(), name=views.ProductListView.name),
    path('api/product/<str:pk>', views.ProductDetail.as_view(), name=views.ProductDetail.name),

    # api categories
    path('api/categories/v1', views.CategoryListView.as_view(), name=views.CategoryListView.name),
    path('api/category/<str:pk>', views.CategoryDetail.as_view(), name=views.CategoryDetail.name),
]
