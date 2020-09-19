from rest_framework import serializers
# from collections import OrderedDict

# Product
from product.models import Brand,Product
class BrandSerializer(serializers.ModelSerializer):
	class Meta:
		model 	= Brand
		fields 	= '__all__'

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model 	= Product
		fields 	= '__all__'

# Sale
from sale.models import Sale
class SaleSerializer(serializers.ModelSerializer):
	class Meta:
		model 	= Sale
		fields 	= '__all__'