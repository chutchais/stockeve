from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import (ExpressionWrapper,F,Min,Max,Avg,StdDev,Count,Sum,
							Value, When,Case,IntegerField,CharField,FloatField)
from django.db.models.signals import post_save,pre_save,pre_delete
# Create your models here.
from store.models 		import Store
from product.models 	import Product,ProductStock
# from receiving.tasks	import add_to_receive

from django_q.tasks import async_task

class Receiving(models.Model):
	store 			= models.ForeignKey(Store, null=True,blank = True,
					on_delete=models.SET_NULL,
					related_name='receivings')
	product 		= models.ForeignKey(Product, null=True,blank = True,
					on_delete=models.SET_NULL,
					related_name='receivings')
	productstock 	= models.ForeignKey(ProductStock, null=True,blank = True,
					on_delete=models.SET_NULL,
					related_name='receivings')
	description 	= models.TextField(max_length=500,blank=True, null=True)
	qty 			= models.IntegerField(default=0)
	inspected   	= models.BooleanField(default=False)
	created 		= models.DateTimeField(auto_now_add=True)#Receiving Date
	updated 		= models.DateTimeField(auto_now=True)
	status 			= models.BooleanField(default=True)
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,blank=True,null=True)
	receivedate 	= models.DateTimeField(null=True,blank=True)

	def __str__(self):
		return f'{self.product} on {self.store}'

	def get_absolute_url(self):
		return reverse('receiving:detail', kwargs={'pk': self.pk})

	@property
	def total_inspect(self):
		qty = self.inspections.aggregate(total=Sum('passed'))['total']
		return qty
	total_inspect.fget.short_description = "Total Inspection"

	def clean(self):
	# Don't allow draft entries to have a pub_date.
		#  QTY must grater than Zero
		if self.qty <= 0  :
			raise ValidationError(_('Qty must be greater than Zero'))

		if not self.store :
			raise ValidationError(_('Store is required'))

		#  Added by Chutchai on July 23,2020
		# To allow only Child product
		if self.product.childs.count() > 0  :
			raise ValidationError(_('Not allow to receive TOP product'))

	def save(self, *args, **kwargs):
		#check if obj is new or being updated
		try:
			print('On save function',self.status)
			if True :
				obj, created = ProductStock.objects.get_or_create(
					    store = self.store,
					    product=self.product,
					    defaults= {'qty' : self.qty}
					)
			if not created:
				obj.qty = obj.qty + self.qty
				obj.save()
				
			self.productstock = obj
			self.status = False
		except ObjectDoesNotExist:
			pass
		#call super and store data
		super(Receiving, self).save(*args, **kwargs)

		
def pre_save_receiving_receiver(sender, instance, *args, **kwargs):
	if instance.status :
		obj, created = ProductStock.objects.get_or_create(
			    store = instance.store,
			    product=instance.product,
			    defaults= {'qty' : instance.qty}
			)
		if not created:
			obj.qty = obj.qty + instance.qty
			obj.save()
			
		instance.productstock = obj
		instance.status = False

def pre_delete_receiving_receiver(sender, instance, *args, **kwargs):
	if not instance.inspected :
		try:
			objs = ProductStock.objects.filter(
			    store = instance.store,
			    product=instance.product
			    )
			if objs :
				for obj in objs:
					obj.qty = obj.qty - instance.qty
					obj.save()
		except ProductStock.DoesNotExist:
			pass
		

	# from django.db.models import Sum
	# x = instance.stocks.filter(store__sale_able=True).aggregate(Sum('qty'))
	# qty = int(x['qty__sum']) if x['qty__sum'] else 0
	# print('Qty : %s - %s on product' % (qty,instance.min_stock) )
	# print(instance.min_stock > qty)
	# instance.lower_stock = instance.min_stock > qty

def post_save_receiving_receiver(sender,created, instance, *args, **kwargs):
	if created :
		print('Create new Receiving')
		# update_min_stock(instance.product)
		async_task('product.tasks.update_min_stock',instance.product)



post_save.connect(post_save_receiving_receiver, sender=Receiving)

pre_delete.connect(pre_delete_receiving_receiver, sender=Receiving)


# 1) Receive (Qty=n, Passed=0) 
# 2) Inspect (Qty=n,Passed=x,Inspected=True)

class Inspection(models.Model):
	receiving 		= models.ForeignKey(Receiving, null=True,blank = True,
						on_delete=models.SET_NULL,
						related_name='inspections')
	qty 			= models.IntegerField(default=0)#Inpect Qty
	passed 			= models.IntegerField(default=0)#Passed
	# Move to Store
	productstock	= models.ForeignKey(ProductStock, 
							null=True,blank = True,
							on_delete=models.SET_NULL,
							related_name='inspections')
	store 			= models.ForeignKey(Store, null=True,blank = True,
						on_delete=models.SET_NULL,
						related_name='inspections')
	note 			= models.CharField(max_length=500,null=True,blank = True)
	created 		= models.DateTimeField(auto_now_add=True)#Receiving Date
	updated 		= models.DateTimeField(auto_now=True)
	status 			= models.BooleanField(default=True)
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL,
						on_delete=models.SET_NULL,blank=True,null=True)

	def __str__(self):
		return f'{self.receiving}'

	def get_absolute_url(self):
		return reverse('receiving:inspect-detail', kwargs={'pk': self.pk})

	def clean(self):
	# Don't allow draft entries to have a pub_date.
		if self.qty <= 0 or self.passed <= 0:
			raise ValidationError(_('QTY or Inspection QTY must be more zero'))
		#  if QTY inspection > QTY Receiving
		if self.qty > self.receiving.qty :
			raise ValidationError(_('Number of Inspection must be less than Receive QTY'))
		#  QTY Passed > QTY Inspection
		if self.passed > self.qty :
			raise ValidationError(_('Number of Passed must be less than inpsect QTY'))

		if not self.store :
			raise ValidationError(_('Store is Required.'))


def pre_save_inspection_receiver(sender, instance, *args, **kwargs):
	print ('Add Inspection :')
	if instance.status :
		# Move Passed to new Store
		obj, created = ProductStock.objects.get_or_create(
			    store = instance.store,
			    product = instance.receiving.product,
			    defaults= {'qty' : instance.passed}
			)
		if not created:
			obj.qty = obj.qty + instance.passed
			obj.save()

		instance.productstock = obj

		

		# Update Original Store(Receiving) (receiving.store + receiving.product )
		try:
			obj2 = ProductStock.objects.get(
					store 	= instance.receiving.store,
					product = instance.receiving.product)
			if obj2 :
				print(obj2.qty,instance.passed)
				obj2.qty = obj2.qty - instance.passed
				obj2.save()
		except ProductStock.DoesNotExist:
			pass
		

		instance.status = False
	# update_stock(instance.receiving.product)
	async_task('product.tasks.update_max_stock',instance.receiving.product)


	# obj, created = ProductStock.objects.get_or_create(
	# 	    store = instance.store,
	# 	    product=instance.product,
	# 	    defaults= {'qty' : instance.qty}
	# 	)
	# if not created:
	# 	obj.qty = obj.qty + instance.qty
	# 	obj.save()





pre_save.connect(pre_save_inspection_receiver, sender=Inspection)



def pre_delete_inspection_receiver(sender, instance, *args, **kwargs):
	print ('Delete Inspection :')
	if not instance.receiving.inspected :
		# Remove from target store
		obj = ProductStock.objects.get(
			    store = instance.store,
			    product = instance.receiving.product
			    )

		obj.qty = obj.qty - instance.passed
		obj.save()

		# Add qty back to receiving
		instance.receiving.productstock.qty = instance.receiving.productstock.qty + instance.passed
		instance.receiving.productstock.save()

pre_delete.connect(pre_delete_inspection_receiver, sender=Inspection)



# def update_stock(product):
# 	print('Update Product Max Stock')
# 	from django.db.models import Sum
# 	x = product.stocks.filter(store__sale_able=True).aggregate(Sum('qty'))
# 	qty = int(x['qty__sum']) if x['qty__sum'] else 0
# 	if product.max_stock > 0 :
# 		product.higher_stock 	= qty > product.max_stock
# 		product.save()

# 	if product.min_stock > 0 :
# 		product.lower_stock 	= product.min_stock > qty
# 		product.save()


# Added by Chutchai on Dec 19,2020
# Model for Winspeed
class PoInvHD(models.Model):
	poinvid 		= models.IntegerField(primary_key=True)
	docuno 			= models.CharField(max_length=50,null=True,blank=True)
	totabaseamnt	= models.FloatField(default=0)
	vatamnt			= models.FloatField(default=0)
	netamnt			= models.FloatField(default=0)
	vendorname 		= models.CharField(max_length=250,null=True,blank=True) 
	receivedate 	= models.DateTimeField(null=True,blank=True)
	created 		= models.DateTimeField(auto_now_add=True)#Receiving Date
	updated 		= models.DateTimeField(auto_now=True)
	status 			= models.BooleanField(default=False)
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,blank=True,null=True)
	executed 		= models.BooleanField(default=False)

	def __str__(self):
		return f'{self.poinvid}'

	def get_absolute_url(self):
		return reverse('receive:poinv', kwargs={'pk': self.pk})

class PoInvDT(models.Model):
	listno				= models.IntegerField()
	poinvid 			= models.ForeignKey(PoInvHD, null=True,blank = True,
							on_delete=models.CASCADE,
							related_name='items')
	goodid 				= models.IntegerField()
	goodcode 			= models.CharField(max_length=100,null=True,blank=True)
	goodname 			= models.CharField(max_length=200,null=True,blank=True)
	goodqty				= models.IntegerField(default=1)
	goodamnt 			= models.FloatField(default=0)
	totalexcludeamnt 	= models.FloatField(default=0)
	# added on Sep 29,2020 -- To record Stock Detail
	inveid				= models.IntegerField(null=True,blank=True)
	invecode			= models.CharField(max_length=50,null=True,blank=True)
	invename			= models.CharField(max_length=250,null=True,blank=True)
	created 			= models.DateTimeField(auto_now_add=True)#Receiving Date
	updated 			= models.DateTimeField(auto_now=True)
	status 				= models.BooleanField(default=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,blank=True,null=True)
	executed 			= models.BooleanField(default=False)

	class Meta:
		unique_together = [['listno', 'poinvid']]

	def __str__(self):
		return f'{self.listno} of {self.poinvid}'

	def get_absolute_url(self):
		return reverse('receive:poinvdt', kwargs={'pk': self.pk})

from product.models import Product,ProductStock
from store.models import Store

def add_to_receive(product_code,store_code,saledate,qty=0,price=0,description=''):
    print(f'Add Receive : {product_code} ,{store_code} ,{qty} ,{price} ,{description}')
    # Verify Product
    product,created = Product.objects.get_or_create(
                            number=product_code,
                            defaults={
                                'finished_goods': True,
                                'title':description,
                                'description':description}
                            )
    # Verify Store
    store,created = Store.objects.get_or_create(
                            name = store_code,
                            defaults ={
                                'title':store_code,
                                'sale_able':True}
                            )
    
    # sale = Sale.objects.create(product=product,
    #                 store=store,qty=qty,
    #                 price=price,description=description,created=saledate,saledate=saledate)

    # Get or Create ProductStock
    productstock,created = ProductStock.objects.get_or_create(
                            product = product,
                            store = store
                            )

    receive = Receiving.objects.create(product=product,
                    productstock = productstock,
                    store=store,qty=qty,
                    receivedate=saledate)
    print('Save Receive successful')
	
def post_save_poinvdt_receiver(sender, instance,created, *args, **kwargs):
	# if not instance.executed :
	if created :
		# async_task('receiving.tasks.add_to_receive',instance.goodcode,instance.invecode,
		# 			instance.poinvid.receivedate,instance.goodqty,
		# 			instance.goodamnt,instance.goodname)
		# WARNING : IF use async task ,sometime found wrong incorrect balance
		add_to_receive(instance.goodcode,instance.invecode,
					instance.poinvid.receivedate,instance.goodqty,
					instance.goodamnt,instance.goodname)
		 
		instance.executed = True
		instance.save()
		# print (f'Saved data of {instance.goodcode} -- {instance.invecode}')

post_save.connect(post_save_poinvdt_receiver, sender=PoInvDT)
