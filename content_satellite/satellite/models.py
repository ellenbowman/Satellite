from django.db import models


class Ticker(models.Model):
	
	ticker_symbol = models.CharField(max_length=5, verbose_name='symbol')
	exchange_symbol = models.CharField(max_length=10, verbose_name='exchange')
	instrument_id = models.IntegerField(default=0)
	num_followers = models.IntegerField(default=0, verbose_name='One followers')
	earnings_announcement = models.DateField(null=True, blank=True, verbose_name='next earnings date')
	daily_percent_change = models.DecimalField(max_digits=11, default=0, decimal_places=2, verbose_name='Daily % change')
	percent_change_historical = models.DecimalField(max_digits=11, decimal_places=3, verbose_name='50D%Change')
	company_name = models.CharField(max_length=120, null=True, blank=True, verbose_name='name')
	notes = models.TextField(max_length=5000, null=True, blank=True, verbose_name='Upcoming coverage')
	scorecards_for_ticker = models.CharField(max_length=200, null=True, blank=True, verbose_name='scorecards for ticker')
	services_for_ticker = models.CharField(max_length=200, null=True, blank=True, verbose_name='services for ticker')	
	tier = models.IntegerField(default=0)
	tier_status = models.CharField(max_length=50, null=True, blank=True, verbose_name='tier status')
	analysts_for_ticker = models.CharField(max_length=500, null=True, blank=True, verbose_name='analysts for ticker')
	
	TEN_PERCENT_PROMISE = 1
	FIVE_AND_THREE = 2
	EARNINGS_PREVIEW = 3
	EARNINGS_REVIEW = 4
	RISK_RATING = 5
	COVERAGE_CHOICES = (
		(TEN_PERCENT_PROMISE, '10% Promise'),
		(FIVE_AND_THREE, '5 and 3'),
		(EARNINGS_PREVIEW, 'Earnings Preview'),
		(EARNINGS_REVIEW, 'Earnings Review'),
		(RISK_RATING, 'Risk Rating'),
		)

	coverage_type = models.IntegerField(default=0, choices=COVERAGE_CHOICES)

	def __unicode__(self):
		return self.ticker_symbol


	class Meta:
		ordering = ['ticker_symbol']


	def scorecards(self):
		""" which scorecards have this ticker? """

		# find the ServiceTakes that have this ticker as a foreign key
		service_takes_on_this_ticker = ServiceTake.objects.filter(ticker=self)

		# of those, find the number of unique scorecards. use set() to avoid
		# counting cases where a scorecard has rec'd a ticker more than once
		scorecards_represented = set()
		for service_take in service_takes_on_this_ticker:
			scorecards_represented.add(service_take.scorecard.pretty_name)

		#return len(scorecards_represented)
		#I would like to return len(scorecards_represented) and the below list of the scorecards
		#like this: (5) Stock Advisor (David), Income Investor ...
		return ", ".join(scorecards_represented)



	def services(self):
		"""how many services have this ticker?"""

		# find the ServiceTakes that have this ticker as a foreign key
		service_takes_on_this_ticker = ServiceTake.objects.filter(ticker=self)

		# of those, find the number of unique services. use set() so that if
		# a service has multiple scorecards (eg supernova & stock advisor),
		# we don't inflate the count
		services_represented = set()
		for service_take in service_takes_on_this_ticker:
			services_represented.add(service_take.scorecard.service.name)

		#return len(services_represented)
		num_services = len(services_represented)
		return num_services


class Service(models.Model):
	name = models.CharField(max_length=50)
	pretty_name = models.CharField(max_length=30)

	def __unicode__(self):
		return self.pretty_name

	class Meta:
		ordering = ['pretty_name']

class Scorecard(models.Model):
	name = models.CharField(max_length=30)
	service = models.ForeignKey(Service)
	pretty_name = models.CharField(max_length=30)

	def __unicode__(self):
		return self.pretty_name

	class Meta:
		ordering = ['pretty_name'] 

class ServiceTake(models.Model):
	is_first = models.BooleanField(default=False)
	is_newest= models.BooleanField(default=False)
	action = models.CharField(max_length=10)
	is_core = models.BooleanField(default=False)
	is_present = models.BooleanField(default=False)
	ticker = models.ForeignKey(Ticker)
	scorecard = models.ForeignKey(Scorecard)
	open_date = models.DateField(null=True, blank=True)
	
	def __unicode__(self):
		return str(self.ticker)

	class Meta:
		ordering = ['scorecard'] 


class Article(models.Model):
	title = models.CharField(max_length=100)
	author = models.CharField(max_length=50)
	date_pub = models.DateTimeField(null=True, blank=True)
	url = models.URLField(max_length=400)
	service = models.ForeignKey(Service)
	ticker = models.ForeignKey(Ticker)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['-date_pub']


TEN_PERCENT_PROMISE = 1
FIVE_AND_THREE = 2
EARNINGS_PREVIEW = 3
EARNINGS_REVIEW = 4
RISK_RATING = 5
COVERAGE_CHOICES = (
	(TEN_PERCENT_PROMISE, '10% Promise'),
	(FIVE_AND_THREE, '5 and 3'),
	(EARNINGS_PREVIEW, 'Earnings Preview'),
	(EARNINGS_REVIEW, 'Earnings Review'),
	(RISK_RATING, 'Risk Rating'),
	)

class CoverageType(models.Model):
	coverage_type = models.IntegerField(choices=COVERAGE_CHOICES)
	ticker = models.ForeignKey(Ticker)
	service = models.ForeignKey(Service)


class BylineMetaData(models.Model):
	byline = models.CharField(max_length=50)
	services = models.CharField(max_length=200, null=True, blank=True,verbose_name='services covered in last year')
	tickers = models.CharField(max_length=1500, null=True, blank=True,verbose_name='tickers covered in the last year')

	def __unicode__(self):
		return self.byline

class AnalystForTicker(models.Model):
	priority = models.CharField(max_length=50)
	service = models.ForeignKey(Service)
	ticker = models.ForeignKey(Ticker)
	guide = models.BooleanField(default=False)

	def __unicode__(self):
		return self.analyst


DATA_HARVEST_TYPE_ARTICLES = 1
DATA_HARVEST_TYPE_MARKET_DATA = 2
DATA_HARVEST_TYPE_EARNINGS_DATES = 3
DATA_HARVEST_TYPE_SCORECARD_RECS = 4
DATA_HARVEST_TYPE_BYLINE_META_DATA = 5


DATA_HARVEST_TYPE_CHOICES = (
    (DATA_HARVEST_TYPE_ARTICLES, 'articles'),
    (DATA_HARVEST_TYPE_MARKET_DATA, 'market performance'),
    (DATA_HARVEST_TYPE_EARNINGS_DATES, 'earnings dates'),
    (DATA_HARVEST_TYPE_SCORECARD_RECS, 'scorecard recs'),
    (DATA_HARVEST_TYPE_BYLINE_META_DATA, 'bylines meta data')
)

class DataHarvestEventLog(models.Model):
	data_type = models.IntegerField(choices=DATA_HARVEST_TYPE_CHOICES, default=DATA_HARVEST_TYPE_ARTICLES)

	date_started = models.DateTimeField(auto_now_add=True)
	date_finished = models.DateTimeField(auto_now=True)

	notes = models.TextField(max_length=5000, null=True, blank=True)

	@property 
	def date_type_pretty_name(self):
		choice_matches = [dht[1] for dht in DATA_HARVEST_TYPE_CHOICES if dht[0]==self.data_type]
		if choice_matches:
			return choice_matches[0]
		return 'unknown type'

	def __unicode__(self):
		return self.date_type_pretty_name + " - " + self.date_started.strftime('%b %M %d')

	class Meta:
		ordering = ['-date_started']