from django.shortcuts import render
from django.views.generic import DetailView,CreateView,UpdateView,DeleteView,ListView
from django.db.models import Q,F
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Sale,SaleChildDetail


class SaleListView(LoginRequiredMixin,ListView):
	model = Sale
	paginate_by = 100
	# def get_queryset(self):
	# 	query = self.request.GET.get('q')
	# 	lacking_stock = self.request.GET.get('lacking')
	# 	over_stock = self.request.GET.get('over')
	# 	if query :
	# 		return Product.objects.filter(Q(number__icontains=query) |
	# 								Q(title__icontains=query) |
	# 								Q(note__icontains=query) |
	# 								Q(description__icontains=query),status=True ).order_by('-updated')
	# 	if lacking_stock :
	# 		return Product.objects.filter(lower_stock = True ,status=True).order_by('number')
	# 	if over_stock :
	# 		return Product.objects.filter(higher_stock = True ,status=True).order_by('number')
	# 	# return Product.objects.none()
	# 	return Product.objects.filter(status=True,finished_goods=True).order_by('-updated')

import xlwt
from django.http import HttpResponse
from .models import Sale,SaleChildDetail


def export_sale_child_xls(request):
	created = request.GET.get('created','today')#default 'today'
	# Modify by Chutchai on July 30,2020
	created = 'today' if created == None or created == '' else created

	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="sale_child.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('sale')

	# Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	
	columns = ['ProductCode','Product', 'Parent', 'Store', 'Qty','Price','SaleName','Balance','Date' ]
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()

	qs = None
	# Query Data
	from datetime import date
	if created == 'today':
		today = date.today()
		qs = SaleChildDetail.objects.filter(created__year=today.year,
							created__month=today.month,
							created__day=today.day).order_by('created')

	if created == 'yesterday':
		import datetime
		today = date.today() - datetime.timedelta(days=1)
		qs = SaleChildDetail.objects.filter(created__year=today.year,
							created__month=today.month,
							created__day=today.day).order_by('created')
	
	if created == 'thisweek':
		import datetime
		date = datetime.date.today()
		start_week = date - datetime.timedelta(date.weekday())
		end_week = start_week + datetime.timedelta(7)
		qs = SaleChildDetail.objects.filter(created__range=[start_week, end_week]).order_by('created')

	if created == 'lastweek':
		import datetime
		date = datetime.date.today()
		date_lastweek = date - datetime.timedelta(days=7)
		start_week = date_lastweek - datetime.timedelta(date_lastweek.weekday())
		end_week = start_week + datetime.timedelta(7)
		print (start_week, end_week)
		# date = end_week + datetime.timedelta(days=1)
		# start_week = date - datetime.timedelta(date.weekday())
		# end_week = start_week + datetime.timedelta(7)
		qs = SaleChildDetail.objects.filter(created__range=[start_week, end_week]).order_by('created')

	if created == 'thismonth':
		today = date.today()
		print('this month',today.year,today.month)
		qs = SaleChildDetail.objects.filter(created__year=today.year,
							created__month=today.month).order_by('created')
		# qs = SaleChildDetail.objects.all()

	if created == 'lastmonth':
		import datetime
		today = date.today().replace(day=1) - datetime.timedelta(days=1)
		print('last month',today)
		qs = SaleChildDetail.objects.filter(created__year=today.year,
							created__month=today.month).order_by('created')
	# print(qs)
	
	for row in qs :
		if row.product.childs.count() > 0:
			# Child level
			for p in row.product.childs.all() :
				row_num += 1
				ws.write(row_num, 0, p.number, font_style)
				ws.write(row_num, 1, str(p), font_style)
				ws.write(row_num, 2, str(row.product), font_style)
				ws.write(row_num, 3, str(row.store), font_style)
				ws.write(row_num, 4, str(row.qty), font_style)
				ws.write(row_num, 5, str(row.price), font_style)
				ws.write(row_num, 6, str(row.salename), font_style)
				ws.write(row_num, 7, str(row.balance), font_style)
				ws.write(row_num, 8, str(row.created), font_style)
		else:
			# Single level
			row_num += 1
			ws.write(row_num, 0, str(row.product.number), font_style)
			ws.write(row_num, 1, str(row), font_style)
			ws.write(row_num, 2, '', font_style)
			ws.write(row_num, 3, str(row.store), font_style)
			ws.write(row_num, 4, str(row.qty), font_style)
			ws.write(row_num, 5, str(row.price), font_style)
			ws.write(row_num, 6, str(row.salename), font_style)
			ws.write(row_num, 7, str(row.balance), font_style)
			ws.write(row_num, 8, str(row.created), font_style)

	wb.save(response)
	return response