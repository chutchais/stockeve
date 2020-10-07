from django.core.mail import send_mail
from django_q.tasks import async_task

def update_min_stock(product):
	print('Update Product Min Stock')
	from django.db.models import Sum

	if product.childs.count() > 0 :
		print(f'{product} has childs')
		# Has Child
		product.lower_stock = product.min_stock > product.total_qty
	else:
		# No Child
		print(f'{product} has no childs')
		x = product.stocks.filter(store__sale_able=True).aggregate(Sum('qty'))
		qty = int(x['qty__sum']) if x['qty__sum'] else 0
		print(f'{product} has available stock : {qty}')
		product.lower_stock = product.min_stock > qty
	# if product.max_stock > 0 :
	# 	product.higher_stock 	= qty > product.max_stock
	# 	product.save()

	if product.min_stock > 0 :
		# product.lower_stock 	= product.min_stock > qty
		product.save()
		# update_min_stock(instance.product)
		async_task('product.tasks.sendemail_if_low_stock',product)


def update_max_stock(product):
	print('Update Product Max Stock')
	from django.db.models import Sum

	x = product.stocks.filter(store__sale_able=True).aggregate(Sum('qty'))
	qty = int(x['qty__sum']) if x['qty__sum'] else 0
	if product.max_stock > 0 :
		product.higher_stock 	= qty > product.max_stock
		product.save()

	# if product.min_stock > 0 :
	# 	product.lower_stock 	= product.min_stock > qty
	# 	product.save()

# Added on Oct 7,2020
# Move function from Model(Pre-save)

def sendemail_if_low_stock(product):
	if product.lower_stock :
		print (f'{product} is low stock -- Send mail')
		from django.template.loader import render_to_string
		html_message  = render_to_string('product/email_lacking_stock.html', 
			{'object': product })

		from django.conf import settings as conf_settings
		recipient_list 	= conf_settings.EMAIL_RECIPIENT_LACKING_LIST
		from_email 		= conf_settings.DEFAULT_FROM_EMAIL

		send_mail(
			subject= f'ALERT! - Lacking stock of : {product.number} ',
			message = None,
			from_email=from_email,
			recipient_list=recipient_list,
			fail_silently=False,
			auth_user=None,auth_password=None,connection=None,
			html_message=html_message
		)