from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import (CategoryViewSet, ProductViewSet, 
                   ProductImageViewSet, ProductVariantViewSet)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet, basename='product')

# Nested routers for product images and variants
products_router = routers.NestedSimpleRouter(router, r'products', lookup='product')
products_router.register(r'images', ProductImageViewSet, basename='product-images')
products_router.register(r'variants', ProductVariantViewSet, basename='product-variants')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
]