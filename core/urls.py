from django.urls import path, include
from .views import *

from rest_framework_simplejwt import views as jwt_views

# Create your urls here.
urlpatterns = [
    #root api
    path('', ApiRoot.as_view(), name=ApiRoot.name),

    # api clients/authentication
    path('api/clients/v1', ClientListView.as_view(), name=ClientListView.name),
    path('api/client/<str:pk>', ClientDetail.as_view(), name=ClientDetail.name),
    path('api/authentication', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
]