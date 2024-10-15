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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path
from rest_framework_simplejwt.authentication import JWTAuthentication
# schema_view = get_schema_view(
#     openapi.Info(
#         title="Fast Food API",
#         default_version='v1',
#         description="Test description",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="support@fastfood.uz"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )
schema_view = get_schema_view(
    openapi.Info(
        title='Chat API',
        description='Chat API',
        default_version="v1",
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
    authentication_classes=[JWTAuthentication,],
)

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
                  path('order/<int:order_id>/change-status/', OrderStatusChangeView.as_view(),
                       name='change-order-status'),
                  path('nearest-branches/', NearestBranchView.as_view(), name='nearest-branches'),
                  path('', include(router.urls)),
                  re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                          name='schema-json'),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
