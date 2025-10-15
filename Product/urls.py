from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from Product.views import ProductViewSet, CategoryViewSet, VariantViewSet, ProductImageViewSet

router = routers.DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"variants", VariantViewSet)
router.register(r"products-images", ProductImageViewSet)

urlpatterns = router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)