from django.shortcuts import render
from .models import Promotion
import datetime

def promotion(request):
	today = datetime.datetime.today()
	promo = Promotion.objects.filter(promotiondate__gte = today).order_by('priority')
	context = {'promo':promo}
	return render(request, 'promotion.html',context)

# Create your views here.
