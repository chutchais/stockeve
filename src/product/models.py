from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save,pre_save

from django.core.mail import send_mail
from store.models import Store

from django.contrib.sites.models import Site

class Brand(models.Model):
	name 				= models.CharField(max_length=500,primary_key=True,
							validators=[
									RegexValidator(
										regex='^[\w-]+$',
										message='Name does not allow special charecters',
									),
								])
	title 				= models.CharField(max_length=500,blank=True, null=True)
	created 			= models.DateTimeField(auto_now_add=True)
	updated 			= models.DateTimeField(blank=True, null=True,auto_now=True)
	status 				= models.BooleanField(default=True)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,blank=True,null=True)

	def __str__(self):
		return f'{self.name}'

	def get_absolute_url(self):
		return reverse('product:brand-detail', kwargs={'id': self.name})



	@property
	def total_product(self):
		qty = self.products.count()
		return qty
	total_product.fget.short_description = "Total product"

class ProductFamily(models.Model):
	name 				= models.CharField(max_length=500,primary_key=True,
							validators=[
									RegexValidator(
										regex='^[\w-]+$',
										message='Name does not allow special charecters',
									),
								])
	title 				= models.CharField(max_length=500,blank=True, null=True)
	created 			= models.DateTimeField(auto_now_add=True)
	updated 			= models.DateTimeField(blank=True, null=True,auto_now=True)
	status 				= models.BooleanField(default=True)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,blank=True,null=True)

	def __str__(self):
		return f'{self.name}'

	def get_absolute_url(self):
		return reverse('product:family-detail', kwargs={'id': self.name})

	@property
	def total_product(self):
		qty = self.products.count()
		return qty
	total_product.fget.short_description = "Total product"


class ProductSubFamily(models.Model):
	name 				= models.CharField(max_length=500,
							validators=[
									RegexValidator(
										regex='^[\w-]+$',
										message='Name does not allow special charecters',
									),
								])
	family 				= models.ForeignKey(ProductFamily, null=True,blank = True,
							on_delete=models.SET_NULL,
							related_name='subfamilies')
	title 				= models.CharField(max_length=500,blank=True, null=True)
	created 			= models.DateTimeField(auto_now_add=True)
	updated 			= models.DateTimeField(blank=True, null=True,auto_now=True)
	status 				= models.BooleanField(default=True)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,blank=True,null=True)

	def __str__(self):
		return '%s : %s' % (self.family,self.name)

	def get_absolute_url(self):
		return reverse('product:subfamily-detail', kwargs={'id': self.name})

	@property
	def total_product(self):
		qty = self.products.count()
		return qty
	total_product.fget.short_description = "Total product"

class Product(models.Model):
	PCS    ='PCS'
	SETS    ='SETS'
	UNIT_NAME_CHOICES = (
	        (PCS, 'Pcs'),
	        (SETS, 'Set'),
	    )
	number 				= models.CharField(max_length=500,primary_key=True,
							validators=[
									RegexValidator(
										regex='^[\w-]+$',
										message='Partnumber does not allow special charecters',
									),
								])
	title 				= models.CharField(max_length=500,blank=True, null=True)
	description 		= models.TextField(max_length=500,blank=True, null=True)
	# parent 				= models.ForeignKey('self', null=True,blank = True,
	# 						on_delete=models.SET_NULL,
	# 						related_name='childs')
	childs 				= models.ManyToManyField('self',blank=True,
							symmetrical=False,related_name = 'parents')
	brand 				= models.ForeignKey(Brand, null=True,blank =True,
							on_delete=models.SET_NULL,
							related_name='products')
	subfamily 			= models.ForeignKey(ProductSubFamily, null=True,blank=True,
							on_delete=models.SET_NULL,
							related_name='products')
	finished_goods 		= models.BooleanField(default=False)
	min_stock 			= models.IntegerField(default=0)
	max_stock 			= models.IntegerField(default=0)
	lower_stock			= models.BooleanField(default=False)
	higher_stock		= models.BooleanField(default=False)
	unit_name 			= models.CharField(max_length=10,choices=UNIT_NAME_CHOICES,default=PCS)
	note 				= models.TextField(null=True,blank = True)
	created 			= models.DateTimeField(auto_now_add=True)
	updated 			= models.DateTimeField(blank=True, null=True,auto_now=True)
	status 				= models.BooleanField(default=True)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,blank=True,null=True)

	def __str__(self):
		return f'{self.number} x {self.title}'

	def get_absolute_url(self):
		return reverse('product:detail', kwargs={'pk': self.pk})

	def get_full_url(self):
		current_site = Site.objects.get_current()
		return f'{current_site.domain}{self.get_absolute_url()}'

	@property
	def total_qty(self):
		from django.db.models import Sum
		if self.childs.count()  == 0 :
			# Child product , QTY will count from all Store.
			qty = self.stocks.filter(store__sale_able=True).aggregate(Sum('qty'))
			return qty['qty__sum'] if qty['qty__sum'] else '0'
		else :
			# Parent product, QTY will sum of all child's qty
			qty = 0
			if self.childs.count() > 0 :
				first = True
				for p in self.childs.all():
					sub_qty = int(p.total_qty)
					if first :
						qty = sub_qty
						first = False
					qty = sub_qty if sub_qty < qty else qty
			# else :
			# 	qty = self.stocks.filter(store__sale_able=True).aggregate(Sum('qty'))
			# 	return qty['qty__sum'] if qty['qty__sum'] else '0'
			# 	# print(qty+p.total_qty)
			return qty
	total_qty.fget.short_description = "Available Stock"

	@property
	def total_unsale_qty(self):
		from django.db.models import Sum

		if self.childs.count() >0 :
			# Sub Product
			qty = self.stocks.filter(store__sale_able=False).aggregate(Sum('qty'))
			return qty['qty__sum'] if qty['qty__sum'] else '0'
		else :
			# Top product, QTY will sum of all child's qty
			# print('Top Product',self.number)
			qty = 0
			if self.childs.count() > 0 :
				print('Has child Product')
				for p in self.childs.all():
					sub_qty = int(p.total_unsale_qty)		
					qty = sub_qty + qty
			else :
				# print('No child Product')
				qty = self.stocks.filter(store__sale_able=False).aggregate(Sum('qty'))
				return qty['qty__sum'] if qty['qty__sum'] else '0'
				# print(qty+p.total_qty)
			return qty
	total_unsale_qty.fget.short_description = "Unsale QTY"

def pre_save_product_receiver(sender, instance, *args, **kwargs):


	from django.db.models import Sum
	if instance.childs.count() > 0 :
		# print('Has child' , instance.total_qty)
		instance.lower_stock = instance.min_stock > instance.total_qty
	else:
		# Top product (No Child)
		x = instance.stocks.filter(store__sale_able=True).aggregate(Sum('qty'))
		qty = int(x['qty__sum']) if x['qty__sum'] else 0
		instance.lower_stock = instance.min_stock > qty

	# Added by Chutchai on Apr 26,2020
	# To Send Email if lower_stock is True
	if instance.lower_stock :
		from django.template.loader import render_to_string
		html_message  = render_to_string('product/email_lacking_stock.html', 
			{'object': instance })

		from django.conf import settings as conf_settings
		recipient_list 	= conf_settings.EMAIL_RECIPIENT_LACKING_LIST
		from_email 		= conf_settings.DEFAULT_FROM_EMAIL

		send_mail(
		subject= f'ALERT! - Lacking stock of : {instance.number} ',
		message = None,
		from_email=from_email,
		recipient_list=recipient_list,
		fail_silently=False,
		auth_user=None,auth_password=None,connection=None,
		html_message=html_message
		)


pre_save.connect(pre_save_product_receiver, sender=Product)


# Product stock for each store
class ProductStock(models.Model):
	store 				= models.ForeignKey(Store, null=True,blank = True,
							on_delete=models.SET_NULL,
							related_name='products')
	product 			= models.ForeignKey(Product, null=True,blank = True,
							on_delete=models.SET_NULL,
							related_name='stocks')
	qty 				= models.IntegerField(default=0)
	note 				= models.TextField(null=True,blank = True)
	created 			= models.DateTimeField(auto_now_add=True)
	updated 			= models.DateTimeField(blank=True, null=True,auto_now=True)
	status 				= models.BooleanField(default=True)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,blank=True,null=True)

	def __str__(self):
		return '%s on %s' % (self.product,self.store)

	def get_absolute_url(self):
		return reverse('product:stock-detail', kwargs={'pk': self.pk})							


def pre_save_productstock_receiver(sender, instance, *args, **kwargs):
	if instance.product :
		instance.product.save()

post_save.connect(pre_save_productstock_receiver, sender=ProductStock)




def image_file_name(instance, filename):
	# return '/'.join(['content', instance.user.username, filename])
	return 'images/product/%s/%s' % (instance.product, filename)

# Support multiple image for each contianer
class ProductImage(models.Model):
	product		= models.ForeignKey(Product,
							blank=True,null=True,
							on_delete=models.SET_NULL,
							related_name = 'images')
	note			= models.CharField(max_length=500,blank=True, null=True)
	file 			= models.ImageField(upload_to=image_file_name)
	created		 	= models.DateTimeField(auto_now_add=True)
	updated     	= models.DateTimeField(blank=True, null=True,auto_now=True)

	def __str__(self):
		return self.product.number

	def get_image_url(self):
		return self.file.url


# class Person(models.Model):
# 	name 	= models.CharField(max_length=100)
# 	friends = models.ManyToManyField("self",blank=True, null=True,
# 							symmetrical=False,related_name = 'parent')
# 	def __str__(self):
# 		return self.name