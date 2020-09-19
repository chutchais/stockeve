from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from product.models import Brand,Product
from .serializers import (BrandSerializer,ProductSerializer,
						SaleSerializer)

# import datetime

class BrandViewSet(viewsets.ModelViewSet):
	queryset = Brand.objects.all()
	serializer_class = BrandSerializer

class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['number', 'title']

# Sale
from sale.models import Sale
class SaleViewSet(viewsets.ModelViewSet):
	queryset = Sale.objects.all()
	serializer_class = SaleSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['product', 'store','salename']
