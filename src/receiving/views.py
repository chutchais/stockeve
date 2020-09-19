from django.shortcuts import render
from django.views.generic import DetailView,CreateView,UpdateView,DeleteView,ListView
from django.db.models import Q,F
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from .models import Receiving

class ReceivingListView(LoginRequiredMixin,ListView):
	model = Receiving
	paginate_by = 100
	def get_queryset(self):
		query 			= self.request.GET.get('q')
		all_receiving 	= self.request.GET.get('all')
		if query :
			return Receiving.objects.filter(Q(product__number__icontains=query) |
									Q(product__title__icontains=query) |
									Q(description__icontains=query),inspected=False, product__finished_goods=True).order_by('-updated')
		if all_receiving :
			return Receiving.objects.filter(product__finished_goods=True).order_by('-updated')

		return Receiving.objects.filter(inspected=False, product__finished_goods=True).order_by('-updated')

class ReceivingDetailView(LoginRequiredMixin,DetailView):
	model = Receiving