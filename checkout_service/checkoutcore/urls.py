from django.urls import path
from checkoutcore.views import *

app_name = 'checkoutcore'


urlpatterns = [
    # Root API
    path('', ApiRoot.as_view(), name=ApiRoot.name),

    # api status
    path('api/status', StatusListView.as_view(), name=StatusListView.name),
    path('api/status/<str:pk>', StatusDetail.as_view(), name=StatusDetail.name),

    # api payment
    path('api/checkouts/v1', CheckoutListCreateView.as_view(), name=CheckoutListCreateView.name),
    path('api/checkout/<str:pk>', CheckoutDetail.as_view(), name=CheckoutDetail.name),
    path('api/checkoutitems/v1', CheckoutItemCreateView.as_view(), name=CheckoutItemCreateView.name),
    path('api/checkoutitem/<str:pk>', CheckoutItemDetail.as_view(), name=CheckoutItemDetail.name),
]
