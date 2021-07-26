from django.urls import include, path
from rest_framework import routers

from . import views

BASE_URL = 'toyrem-api/'

router = routers.DefaultRouter()
router.register(BASE_URL + r'category', views.CategoryViewSet)
router.register(BASE_URL + r'product', views.ProductViewSet)
router.register(BASE_URL + r'productimage', views.ProductImageViewSet)
router.register(BASE_URL + r'cart', views.CartViewSet, basename='Cart')
router.register(BASE_URL + r'cart-item', views.CartItemViewSet, basename='CartItem')
router.register(BASE_URL + r'order', views.OrderViewSet, basename='Order')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]