from rest_framework.routers import DefaultRouter
from page.views import  LoginAPIView, RegisterUserView
from app.branch.api.branch.views import BranchViewSet, NearestBranchViewSet
from app.food.api.food.views import FoodItemViewSet, FoodItemViewSetGet
from app.order.api.order.views import CreateOrderView, AdminOrderViewSet, OrderStatusChangeView
from django.contrib import admin
from qozon import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path ,include

schema_view = get_schema_view(
    openapi.Info(
        title='Chat API',
        description='Chat API',
        default_version="v1",
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

router = DefaultRouter()
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'fooditems', FoodItemViewSet)
router.register(r'fooditems_get', FoodItemViewSetGet, basename='fooditem-get')
router.register(r'nearest-branches', NearestBranchViewSet, basename='nearest-branches')
router.register(r'get-orders', AdminOrderViewSet, basename='get-orders')

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('register/', RegisterUserView.as_view(), name='register'),
                  path('accounts/login/', LoginAPIView.as_view(), name='token_obtain_pair'),
                  path('create-order/', CreateOrderView.as_view(), name='create-order'),
                  path('order/<int:order_id>/change-status/', OrderStatusChangeView.as_view(),
                       name='change-order-status'),
                  path('', include(router.urls)),
                  path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
