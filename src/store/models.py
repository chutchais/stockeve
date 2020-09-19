from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.conf import settings
# Create your models here.


class Store(models.Model):
	name 		= models.CharField(max_length=50,primary_key=True,
					validators=[
							RegexValidator(
								regex='^[\w-]+$',
								message='Name does not allow special charecters',
							),
						])
	title 		= models.CharField(max_length=100,blank=True, null=True)
	description = models.TextField(max_length=255,blank=True, null=True)
	incoming	= models.BooleanField(default=False)
	sale_able	= models.BooleanField(default=False)
	created 	= models.DateTimeField(auto_now_add=True)
	updated 	= models.DateTimeField(auto_now=True)
	status 		= models.BooleanField(default=True)
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,blank=True,null=True)

	def __str__(self):
		return f'{self.name}'

	def get_absolute_url(self):
		return reverse('store:detail', kwargs={'id': self.name})


	@property
	def total_product(self):
		qty = self.products.count()
		return qty
	total_product.fget.short_description = "Total Product in Stock"

