from django.shortcuts import render
from django.http import HttpResponse
from models import Ticker, Service, Scorecard, ServiceTake, Article
from django.http import HttpResponseRedirect
from forms import NotesForm

# Create your views here.

###############################################################################

### will make way for info_by_scorecard or something quite like it

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

###############################################################################


def movers(request):
	# here we practice using 'context'
	context = {
		'pagetitle': "Today's Biggest Movers",
		'tickers': Ticker.objects.all().order_by('ticker_symbol')[:20],
		'scorecards': Scorecard.objects.all().order_by('pretty_name'),
		'biggestmovers': Ticker.objects.all().order_by('-daily_percent_change')[:20],
	}

	return render(request, 'satellite/movers.html', context)


###############################################################################

def articles_by_service(request):
	
	service_name = None
	if 'service' in request.GET:
		service_name = request.GET['service']

	max_count = 20

	if service_name:
		service_match = Service.objects.filter(name=service_name)
		articles = Article.objects.filter(service__in=service_match)[:max_count]
	else:
		articles = Article.objects.all()[:max_count]

# ServiceTakes have both a ticker and a scorecard, and a scorecard has a service.
# So show me ServiceTakes by scorecard?

	dictionary_of_values = {
		'articles' : articles,
		'service_name': service_name,
		'articles_max_count': max_count
	}

	return render(request, 'satellite/articles_by_service.html', dictionary_of_values)

	
###############################################################################

def info_by_scorecard(request):
	
	scorecard_name = None
	# let's see if the user passed along a 'scorecard' in the query string
	if 'scorecard' in request.GET:
		scorecard_name = request.GET['scorecard']
		# i see a match! let's store it in a local variable
		# (ie exists only for the life of this function) called 'scorecard_name'
		# eb: below I made it a global variable, I believe, so I could put it
		# into the html view


	# and now, let's see if there's anything interesting in the PUT dictionary
	# one use case of the PUT dictionary: from form actions, where data is passed 
	# along in the request, just not as a query string
	if request.POST:
		
		# find the keys that correspond to the 'notes' input. 
		# since we also have control over the forms markup (embedded in 'info_by_scorecard.html'), 
		# we know that the form data we're interested in has names that start with 'ticker_notes_'.
		# it translates that these names should be visible as keys in the request.POST dictionary

		ticker_note_name_prefix = 'ticker_notes_'

		# use 'python list comprehension' to create a list of all the keys in request.POST that 
		# match this condition: the key must start with 'ticker_notes_' . equivalent to a multi-line
		# 'for' loop.
		keys_of_ticker_note_data = [key_in_post_dict for key_in_post_dict in request.POST.keys() if key_in_post_dict.startswith(ticker_note_name_prefix)]
		
		for key_of_ticker_note_data in keys_of_ticker_note_data:
			# from each key, we can extract the Ticker id that we've embedded in the key
			# (eg, if we see 'ticker_notes_3', we know it corresponds to the Ticker with id 3)
			# and we can use that id to retrieve the Ticker object from the db,
			# update its notes field, and save the Ticker. voila!

			ticker_id = key_of_ticker_note_data[len(ticker_note_name_prefix):]  # pick out everything in the string that follows the 'ticker_notes_' prefix
			ticker_to_update = Ticker.objects.get(id=ticker_id)

			ticker_to_update.notes = request.POST[key_of_ticker_note_data] # retrieve from the POST dictionary the user input corresponding to this Ticker object
			ticker_to_update.save() # write this update to the db!
			
			# print to console a sanity check
			print 'updated Ticker %s (id: %s). notes value: %s' % (ticker_to_update.ticker_symbol, ticker_id, ticker_to_update.notes)  


	max_count = 10

# so the below is showing us all the tickers in the Pro scorecard.

	if scorecard_name:
		scorecard_match = Scorecard.objects.filter(pretty_name=scorecard_name)
		print 'any matches?', len(scorecard_match), scorecard_match, '!!!!!!!!!!!!!!!!!'
		scorecard_take = ServiceTake.objects.filter(scorecard__in=scorecard_match) #[:max_count]

	else:
		scorecard_take = ServiceTake.objects.all() #[:max_count]	

		# so now you have ServiceTake objects that are associated with the Scorecard objects
		# that have name 'Pro' -- below it prints the number of 'em in the terminal

	print 'how many scorecard_take ?', len(scorecard_take), '!!!!!!!!!!!!'


# now, to get the ticker symbols associated with ServiceTake objects?
# how about a "for" loop that collects the value of the 'ticker' field from each ServiceTake?


	ticker_matches = set()
	for st in scorecard_take:
		ticker_matches.add(st.ticker)
		# print 'what is the ticker?', st, '!!!!!!!!'

	# that's all we need. but let's refine things. let's alphabetize the tickers.
    # while a 'set' is convenient because we'll avoid duplicates,
    # sets don't have a sense of ordering. lists have a sense of ordering.
    # let's convert the set to a list and sort it.


	ticker_matches_list = list(ticker_matches)
	print 'ticker matches:', len(ticker_matches_list), '------------------'
	ticker_matches_list.sort(key=lambda x: x.daily_percent_change, reverse=True)

	dictionary_of_values = {
		'scorecard_take' : scorecard_take,
		'ticker_matches_list' : ticker_matches_list,
		}
	

	return render(request, 'satellite/info_by_scorecard.html', dictionary_of_values)	


#############################################################################
 
def edit_notes_page(request):
	# if this is a POST request we need to process the form data
    if request.method == 'POST':
    # create a form instance and populate it with data from the request:
       form = NotesForm(request.POST)
       # check whether it's valid:
       if form.is_valid():
       		# process the data in form.cleaned_data as required
       		# ...
       		# ... redirect to a new URL:
            return HttpResponseRedirect('/sol/edit_notes_page/')
        	# if a GET (or any other method) we'll create a blank form
    else:
    	form = NotesForm()

    return render(request, 'satellite/edit_notes_page.html', { 'form': form}) #sol/edit_notes_page


###############################################################################

def scorecard_index(request):
	"""
	a listing of the scorecards, ordered by pretty name
	"""

	all_scorecards = Scorecard.objects.all().order_by('pretty_name')

	dictionary_of_values = {
		'scorecards_in_alpha_order' : all_scorecards,
	}

	return render(request, 'satellite/scorecard_index.html', dictionary_of_values)

###############################################################################