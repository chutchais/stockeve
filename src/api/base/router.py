from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'brand', views.BrandViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'sale', views.SaleViewSet)
# router.register(r'books', views.BookViewSet)

api_urlpatterns = router.urls