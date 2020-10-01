def update_min_stock(product):
	print('Update Product Min Stock')
	from django.db.models import Sum
	x = product.stocks.filter(store__sale_able=True).aggregate(Sum('qty'))
	qty = int(x['qty__sum']) if x['qty__sum'] else 0
	if product.max_stock > 0 :
		product.higher_stock 	= qty > product.max_stock
		product.save()

	if product.min_stock > 0 :
		product.lower_stock 	= product.min_stock > qty
		product.save()


def update_max_stock(product):
	print('Update Product Max Stock')
	from django.db.models import Sum
	x = product.stocks.filter(store__sale_able=True).aggregate(Sum('qty'))
	qty = int(x['qty__sum']) if x['qty__sum'] else 0
	if product.max_stock > 0 :
		product.higher_stock 	= qty > product.max_stock
		product.save()

	if product.min_stock > 0 :
		product.lower_stock 	= product.min_stock > qty
		product.save()