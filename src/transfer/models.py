from django.db import models

# Create your models here.

# Added by Chutchai on Jan 19,2021
# Model for Winspeed
class ICStockHD(models.Model):
	docuid 		    = models.IntegerField(primary_key=True)
	docuno 			= models.CharField(max_length=50,null=True,blank=True)
    remark1         = models.CharField(max_length=255,null=True,blank=True)
	docudate 		= models.DateTimeField(null=True,blank=True)
	created 		= models.DateTimeField(auto_now_add=True)#Receiving Date
	updated 		= models.DateTimeField(auto_now=True)
	status 			= models.BooleanField(default=False)
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,blank=True,null=True)
	executed 		= models.BooleanField(default=False)

	def __str__(self):
		return f'{self.docuid}'

	def get_absolute_url(self):
		return reverse('transfer:icstockhd', kwargs={'pk': self.pk})

class ICStockDetail(models.Model):
	listno				= models.IntegerField()
	icstockhd			= models.ForeignKey(ICStockHD, null=True,blank = True,
							on_delete=models.CASCADE,
							related_name='items')
	goodid 				= models.IntegerField()
	goodcode 			= models.CharField(max_length=100,null=True,blank=True)
	goodname 			= models.CharField(max_length=200,null=True,blank=True)
	goodqty				= models.IntegerField(default=0)
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
		unique_together = [['listno', 'icstockhd']]

	def __str__(self):
		return f'{self.listno} of {self.icstockhd}'

	def get_absolute_url(self):
		return reverse('transfer:icstockdetail', kwargs={'pk': self.pk})

# def post_save_soinvdt_receiver(sender, instance,created, *args, **kwargs):
# 	# if not instance.executed :
# 	if created :
# 		async_task('sale.tasks.add_to_sale',instance.goodcode,instance.invecode,
# 					instance.soinvid.saledate,instance.goodqty,
# 					instance.goodamnt,instance.goodname)
# 		instance.executed = True
# 		instance.save()
# 		# print (f'Saved data of {instance.goodcode} -- {instance.invecode}')

# post_save.connect(post_save_soinvdt_receiver, sender=SoInvDT)
