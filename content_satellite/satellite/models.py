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

	def __unicode__(self):
		return self.ticker_symbol


	class Meta:
		ordering = ['ticker_symbol']


	def scorecards(self):
		""" which scorecards have this ticker? """

		service_takes_on_this_ticker = ServiceTake.objects.filter(ticker=self)

		scorecards_represented = set()
		for service_take in service_takes_on_this_ticker:
			scorecards_represented.add(service_take.scorecard.pretty_name)
		return ", ".join(scorecards_represented)

	def services(self):
		"""how many services have this ticker?"""

		service_takes_on_this_ticker = ServiceTake.objects.filter(ticker=self)

		services_represented = set()
		for service_take in service_takes_on_this_ticker:
			services_represented.add(service_take.scorecard.service.name)

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
RISK_RATING = 2
GUIDANCE_CHANGE = 3
FIVE_AND_THREE = 4
TEN_PERCENT_POTENTIAL = 5
TWO_MINUTE_DRILL = 6
BEST_BUYS_NOW = 7
EARNINGS_PREVIEW = 8
EARNINGS_REVIEW = 9
FOOL_DOT_COM_PREVIEW = 10
FOOL_DOT_COM_REVIEW = 11

COVERAGE_CHOICES = (
	(TEN_PERCENT_PROMISE, '10% Promise'),
	(RISK_RATING, 'Risk Rating'),
	(GUIDANCE_CHANGE, 'Guidance Change'),
	(FIVE_AND_THREE, '5 and 3'),
	(TEN_PERCENT_POTENTIAL, '10% Potential'),
	(TWO_MINUTE_DRILL, '2-Minute Drill'),
	(BEST_BUYS_NOW, 'Best Buys Now'),
	(EARNINGS_PREVIEW, 'Team Preview'),
	(EARNINGS_REVIEW, 'Team Review'),
	(FOOL_DOT_COM_PREVIEW, 'Fool.com Preview'),
	(FOOL_DOT_COM_REVIEW, 'Fool.com Review'),
	)

class CoverageType(models.Model):
	coverage_type = models.IntegerField(choices=COVERAGE_CHOICES, null=True)
	ticker = models.ForeignKey(Ticker)
	service = models.ForeignKey(Service)
	author = models.CharField(max_length=100, null=True, blank=True, verbose_name='Analyst')

	def __unicode__(self):
		return str(self.coverage_type)


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