from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from page.models import User
from page.views import *
from app.branch.api.branch.views import BranchViewSet, NearestBranchView
from app.food.api.food.views import FoodItemViewSet, FoodItemViewSetGet
from app.order.api.order.views import CreateOrderView, AdminOrderListView, OrderStatusChangeView

from django.contrib import admin
from django.urls import path
from qozon import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'fooditems', FoodItemViewSet)
router.register(r'fooditems_get', FoodItemViewSetGet, basename='fooditem-get')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_user),
    path('login/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('get-orders/', AdminOrderListView.as_view(), name='get-orders'),
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('order/<int:order_id>/change-status/', OrderStatusChangeView.as_view(), name='change-order-status'),
    path('nearest-branches/', NearestBranchView.as_view(), name='nearest-branches'),
    path('', include(router.urls)),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
