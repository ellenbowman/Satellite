from django.shortcuts import render
from django.http import HttpResponse
from models import Ticker, Service, Scorecard, ServiceTake

# Create your views here.
def index(request):
	context = {
		'page-title': 'Satellite'
	}


	return HttpResponse("""
		<div align='center'; style='font-family:Verdana, Arial, Helvetica, sans-serif'>
		<p><a href='/admin/satellite/ticker/'><img width='700px' src='http://g.foolcdn.com/editorial/images/150992/welcome_large.png'/></a></p>
		<p><a href="http://satellite.fool.com/admin/satellite/">Other views</a></p>
		</div>
		""", context)




def movers(request):
	context = {
		'pagetitle': "Today's Biggest Movers",
		'tickers': Ticker.objects.all().order_by('ticker_symbol')[:10],
		'scorecards': Scorecard.objects.all().order_by('pretty_name'),
		'biggestmovers': Ticker.objects.all().order_by('-daily_percent_change')[:20],
	}
	return render(request, 'satellite/movers.html', context)