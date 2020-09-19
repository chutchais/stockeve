from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

def pro_img(instance, filename):
	return 'promotion/%s/%s' % (instance.promotion_name, filename)

class Promotion(models.Model):
	promotion_name = models.CharField(max_length=100)
	promotion_detail = RichTextUploadingField(null=True, blank=True)
	promotiondate = models.DateField(null=True, blank=True)
	priority = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)

	def __str__(self):
		return self.promotion_name
# Create your models here.
