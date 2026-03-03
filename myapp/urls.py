from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import*
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'shops', ShopViewSet, basename='shops')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'inventory', InventoryViewSet, basename='inventory')
router.register(r'auth', AuthViewSet, basename='auth')
urlpatterns = [
     path('search/', GlobalSearchView.as_view(), name='global-search'),
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]