from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	context = {
		'page-title': 'Satellite'
	Ticker.fields['ticker_symbol','company_name','exchange_symbol','services','scorecards','num_followers',
	'earnings_announcement'].widget.attrs['readonly'] = True
	}


	return HttpResponse("""
		<div align='center'; style='font-family:Verdana, Arial, Helvetica, sans-serif'>
		<p><a href='/admin/satellite/ticker/'><img width='700px' src='http://g.foolcdn.com/editorial/images/150992/welcome_large.png'/></a></p>
		<p><a href="http://satellite.fool.com/admin/satellite/">Other views</a></p>
		</div>
		""", context)




def editors(request):
	context = {
		'page-title': 'Satellite'
	}
	return render(request, 'satellite/editors.html', context)

	#font-size:35px
	#<p><a href='/admin/satellite'><img width='700px' src='http://g.foolcdn.com/editorial/images/150992/welcome_large.png'/></a></p>
