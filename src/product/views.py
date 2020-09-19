from django.shortcuts import render
from django.views.generic import DetailView,CreateView,UpdateView,DeleteView,ListView
from django.db.models import Q,F
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Product,ProductStock


class ProductListView(LoginRequiredMixin,ListView):
	model = Product
	paginate_by = 100
	def get_queryset(self):
		query = self.request.GET.get('q')
		lacking_stock = self.request.GET.get('lacking')
		over_stock = self.request.GET.get('over')
		if query :
			return Product.objects.filter(Q(number__icontains=query) |
									Q(title__icontains=query) |
									Q(note__icontains=query) |
									Q(description__icontains=query),status=True ).order_by('-updated')
		if lacking_stock :
			return Product.objects.filter(lower_stock = True ,status=True).order_by('number')
		if over_stock :
			return Product.objects.filter(higher_stock = True ,status=True).order_by('number')
		# return Product.objects.none()
		return Product.objects.filter(status=True,finished_goods=True).order_by('-updated')

class ProductDetailView(LoginRequiredMixin,DetailView):
	model = Product


# ProductStock
class ProductStockListView(LoginRequiredMixin,ListView):
	model = ProductStock
	paginate_by = 100
	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return ProductStock.objects.filter(Q(store__name__icontains=query) |
									Q(product__number__icontains=query) |
									Q(note__icontains=query) ).order_by('store')
		# return Product.objects.none()
		return ProductStock.objects.all().order_by('-updated')

class ProductStockDetailView(LoginRequiredMixin,DetailView):
	model = ProductStock