from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse
from models import Article, Service



def services_index(request):
	"""
	a listing of the services, ordered by pretty name
	"""

	all_services = Service.objects.all().order_by('pretty_name')

	dictionary_of_values = {
		'services_in_alpha_order':all_services,
	}

	return render(request, 'satellite/all_the_services.html', dictionary_of_values)



def my_sample_view(request):
	"""
	in this view we practice pulling values from the query string
	and rendering a template that looks up
	values from a dictionary compiled within this view
	"""

	fav_color = 'probably green'
	if 'fav_color' in request.GET:
		fav_color = request.GET['fav_color']

	
	fav_service = 'i like them all!'
	if 'fav_service' in request.GET:
		fav_service = request.GET['fav_service']


	dictionary_of_values = {
		'fav_color' : fav_color,
		'fav_service': fav_service
	}
	return render(request, 'satellite/my_gorgeous_page.html', dictionary_of_values)



def articles_by_service(request):
	
	service_name = None
	# let's see if the user passed along a 'service' in the query string
	if 'service' in request.GET:
		service_name = request.GET['service']

	max_count = 20

	# if we happen to have the local variable called 'service_name', 
	# let's user it to filter the articles
	if service_name:
		# we happen to have the local variable! let's get all Service objects that have a 
		# name that matches the value of service_name
		# capture those Service object matches into a variable named 'service_match'
		service_match = Service.objects.filter(name=service_name)

		# we've identified the service(s) that satisfy our constraint. 
		# let's now query for all Article objects whose service field references a Service object in our service_match.
		articles = Article.objects.filter(service__in=service_match)[:max_count]
	else:
		articles = Article.objects.all()[:max_count]

	

	dictionary_of_values = {
		'articles' : articles,
		'service_name': service_name,
		'articles_max_count': max_count
	}

	return render(request, 'satellite/my_awesome_articles.html', dictionary_of_values)


def extra_views_homepage(request):
	"""
	show a page with links to the views defined in this file
	"""
	return render(request, 'satellite/extra_pages.html')


def grand_vision_articles(request):
	"""
	shows all articles and some meta data
	(time range of the articles, unique authors)

	contains a form that lets you specify tickers and services

	if a service name is detected in the request's GET or POST dictionary, then filters to articles for that service
	if a ticker is detected in the request's GET or POST dictionary, then filters to articles on that ticker
	"""

	# let's sort the articles by descending date (most recent first)
	articles = Article.objects.all().order_by('-date_pub')

	# introduce django's built-in pagination!! let each page show 30 articles
	# https://docs.djangoproject.com/en/1.7/topics/pagination/
	paginator = Paginator(articles, 30) 

	# let's see if the query string already has a value for which 
	# page we should show (eg: '/sol/articles_vomit/?page=4')
	# this could be introduced by the user or by a link on our page
	page_num = request.GET.get('page')

	try:
		articles_subset = paginator.page(page_num)
	except PageNotAnInteger:
		# page is not an integer; let's show the first page of results
		articles_subset = paginator.page(1)
	except EmptyPage:
		# the user asked for a page way beyond what we have available;
		# let's show the last page of articles, which we can calculate
		# with paginator.num_pages
		articles_subset = paginator.page(paginator.num_pages)


	# compile meta data -------------------
	## we already sorted the articles by pub date. to get the newest and oldest, 
	## we just look at the first element in the list, and the last element
	article_most_recent_date = articles[0].date_pub  
	article_oldest_date = articles[len(articles)-1].date_pub

	## how many authors?
	authors = [art.author for art in articles]
	'''  the above line is equivalent to the bottom 3! an example of "list comprehension"
	authors = []
	for art in articles:
		authors.append(art.author)
	'''
	## convert into a set, so that we toss out duplicates
	authors_set = set(authors)
	num_authors = len(authors_set)


	dictionary_of_values = {
		'articles': articles_subset,
		'pub_date_newest': article_most_recent_date,
		'pub_date_oldest': article_oldest_date,
		'num_authors' : num_authors,
	}
	return render(request, 'satellite/index_of_articles.html', dictionary_of_values)
