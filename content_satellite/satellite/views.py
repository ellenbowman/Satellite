from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return HttpResponse("""
		<p style='font-family:"Lucida Console", Monaco, monospace; font-size:35px'>
		coming soon:  <strong>Satellite of Love</strong>
		<br/>
		<br/>Get excited!
		<br/><a href='/admin'><img src='https://tsotniashvili.files.wordpress.com/2011/04/funny-cat-faces-2.jpg'/></a>
		""")
