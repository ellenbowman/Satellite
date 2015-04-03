from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return HttpResponse("""
		<p style='font-family:"Lucida Console", Monaco, monospace; font-size:35px'>
		coming soon:  <strong>Satellite of Love</strong>
		<br/>
		<br/>Get excited!
		<br/><a href='/admin/satellite'><img src='https://fbcdn-sphotos-h-a.akamaihd.net/hphotos-ak-xaf1/t31.0-8/11092652_797813696962016_8473060809451116005_o.jpg' width="500"/></a>
		""")
