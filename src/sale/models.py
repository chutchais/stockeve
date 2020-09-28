from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.conf import settings
from django.db.models.signals import post_save,pre_save,pre_delete

# Create your models here.
from store.models import Store
from product.models import Product,ProductStock

class Sale(models.Model):
	store 			= models.ForeignKey(Store, null=True,blank = True,
							on_delete=models.SET_NULL,
							related_name='sales')
	product 		= models.ForeignKey(Product, null=True,blank = True,
							on_delete=models.SET_NULL,
							related_name='sales')
	productstock	= models.ForeignKey(ProductStock, null=True,blank = True,
							on_delete=models.SET_NULL,
							related_name='sales')
	description 	= models.TextField(max_length=255,blank=True, null=True)
	qty 			= models.IntegerField(default=1)
	price 			= models.FloatField(default=0)
	salename 		= models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,blank=True,null=True,
							related_name='sales')
	balance 		= models.IntegerField(default=0)
	created 		= models.DateTimeField(auto_now_add=True)#Receiving Date
	updated 		= models.DateTimeField(auto_now=True)
	status 			= models.BooleanField(default=False)
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,blank=True,null=True)

	def __str__(self):
		return f'{self.product}'

	def get_absolute_url(self):
		return reverse('sale:detail', kwargs={'pk': self.pk})

	# def save(self, *args, **kwargs):
	#     # Check how the current values differ from ._loaded_values. For example,
	#     # prevent changing the creator_id of the model. (This example doesn't
	#     # support cases where 'creator_id' is deferred).
	#     if not self.product.finished_goods :
	#         raise ValidationError(_("Non finished goods product isn't allowed for Sale"))
	#     super().save(*args, **kwargs)
	def clean(self):
	# Don't allow draft entries to have a pub_date.
		#  Allow only "sale_able" store to be sale.
		if not self.store.sale_able :
			raise ValidationError(_('This store isn''t for Sale.'))

		#  Allow only "Finished Good" product to be sale.
		if not self.product.finished_goods :
			raise ValidationError(_('Non finished goods product isn''t allowed for Sale.'))

		#  Sale QTY must less than Available QTY (product.total_qty)
		if self.qty > int(self.product.total_qty) :
			raise ValidationError(_('Available stock is not enough for this sale. (%s in stock)' % self.product.total_qty))

		#Product is available on Store
		if self.product.childs.count() == 0 :
			ps = ProductStock.objects.filter(product=self.product,store=self.store)
			if not ps:
				raise ValidationError(_('No product %s ,available in %s' % (self.product,self.store)))

	# def save(self, *args, **kwargs):
	# 	pass

def pre_save_sale_receiver(sender, instance, *args, **kwargs):
	if not instance.status :
		try:

			# Update Child product
			if instance.product.childs.count() > 0 :
				for p in instance.product.childs.all() :
					try:
						# objp = ProductStock.objects.filter(
						# 	product=p , store__sale_able = True
						# 	).order_by('qty')
						print('Sale from %s' % instance.store )
						objp = ProductStock.objects.filter(
							product=p , store = instance.store
							).order_by('qty')
					except ProductStock.DoesNotExist:
						objp = None
					
					if objp :
						product_stock = objp.first()
						product_stock.qty = product_stock.qty - instance.qty if (product_stock.qty - instance.qty) >= 0 else 0
						# objp.update()
						product_stock.save()
			else :
				# Top Or No sub product.
				# objp = ProductStock.objects.filter(
				# 			product=instance.product , store__sale_able = True
				# 			).order_by('qty')
				# Modify on Sep 24,2020
				# Sale not adjust correct Store
				print('Sale from %s' % instance.store )
				objp = ProductStock.objects.filter(
							product=instance.product , store=instance.store
							).order_by('qty')
				if objp :
						product_stock = objp.first()
						product_stock.qty = product_stock.qty - instance.qty if (product_stock.qty - instance.qty) >= 0 else 0
						# objp.update()
						product_stock.save()

			# --------------------
			instance.balance 	= instance.product.total_qty
			instance.status 	= True
			# Added by Chutchai on June 14,2020
			#To stamp product stock on Sale
			if objp :
				# instance.store = objp.first().store
				instance.productstock = objp.first()

			update_min_stock(instance.product)

		except ProductStock.DoesNotExist:
			obj = None

		

pre_save.connect(pre_save_sale_receiver, sender=Sale)

def pre_delete_sale_receiver(sender, instance, *args, **kwargs):
	if instance.status :
		try:
			if instance.productstock and instance :
				instance.productstock.qty = instance.productstock.qty + instance.qty
				instance.productstock.save()
				# Update Child product
				if instance.productstock.product :
					for p in instance.productstock.product.childs.all() :
						try:
							objp = ProductStock.objects.get(
								store = instance.productstock.store,
								product=p
								)
						except ProductStock.DoesNotExist:
							objp = None
						
						if objp :
							objp.qty = objp.qty + instance.qty 
							objp.save()

					update_min_stock(instance.productstock.product)
			# --------------------
		except ProductStock.DoesNotExist:
			obj = None
		

# pre_delete.connect(pre_delete_sale_receiver, sender=Sale)


def update_min_stock(product):
	print('Update Product Stock')
	from django.db.models import Sum
	x = product.stocks.filter(store__sale_able=True).aggregate(Sum('qty'))
	qty = int(x['qty__sum']) if x['qty__sum'] else 0
	if product.max_stock > 0 :
		product.higher_stock 	= qty > product.max_stock
		product.save()

	if product.min_stock > 0 :
		product.lower_stock 	= product.min_stock > qty
		product.save()
		
	# product.lower_stock 	= product.min_stock > qty
	# product.higher_stock 	= qty > product.max_stock
	# product.save()



# def pre_save_sale_receiver(sender, instance, *args, **kwargs):
# 	if not instance.status :
# 		try:
# 			instance.productstock.qty = instance.productstock.qty - instance.qty if (instance.productstock.qty - instance.qty) >= 0 else 0
# 			instance.productstock.save()
# 			# Update Child product
# 			for p in instance.productstock.product.childs.all() :
# 				try:
# 					objp = ProductStock.objects.get(
# 						store = instance.productstock.store,
# 						product=p
# 						)
# 				except ProductStock.DoesNotExist:
# 					objp = None
				
# 				if objp :
# 					objp.qty = objp.qty - instance.qty if (objp.qty - instance.qty) >= 0 else 0
# 					# objp.update()
# 					objp.save()

# 			# --------------------
# 			instance.balance 	= instance.productstock.qty
# 			instance.status 	= True

# 			update_min_stock(instance.productstock.product)

# 		except ProductStock.DoesNotExist:
# 			obj = None


# Report
class SaleChildDetail(Sale):
    class Meta:
        proxy = True
        verbose_name = 'Child Product Sale Summary'
        verbose_name_plural = 'Child Product Sales Summary'

# Added by Chutchai on Sep 26,2020
# Model for Winspeed
class SoInvHD(models.Model):
	soinvid 		= models.IntegerField(primary_key=True)
	docuno 			= models.CharField(max_length=50,null=True,blank=True)
	totabaseamnt	= models.FloatField(default=0)
	vatamnt			= models.FloatField(default=0)
	netamnt			= models.FloatField(default=0)
	saledate 		= models.DateTimeField(null=True,blank=True)
	created 		= models.DateTimeField(auto_now_add=True)#Receiving Date
	updated 		= models.DateTimeField(auto_now=True)
	status 			= models.BooleanField(default=False)
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,blank=True,null=True)
	executed 		= models.BooleanField(default=False)

	def __str__(self):
		return f'{self.soinvid}'

	def get_absolute_url(self):
		return reverse('sale:soinv', kwargs={'pk': self.pk})

class SoInvDT(models.Model):
	listno				= models.IntegerField()
	soinvid 			= models.ForeignKey(SoInvHD, null=True,blank = True,
							on_delete=models.CASCADE,
							related_name='items')
	goodid 				= models.IntegerField()
	goodcode 			= models.CharField(max_length=100,null=True,blank=True)
	goodname 			= models.CharField(max_length=200,null=True,blank=True)
	goodqty				= models.IntegerField(default=1)
	goodamnt 			= models.FloatField(default=0)
	totalexcludeamnt 	= models.FloatField(default=0)
	created 			= models.DateTimeField(auto_now_add=True)#Receiving Date
	updated 			= models.DateTimeField(auto_now=True)
	status 				= models.BooleanField(default=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,blank=True,null=True)
	executed 			= models.BooleanField(default=False)

	class Meta:
		unique_together = [['listno', 'soinvid']]

	def __str__(self):
		return f'{self.listno} of {self.soinvid}'

	def get_absolute_url(self):
		return reverse('sale:soinvdt', kwargs={'pk': self.pk})