from django.db import models

class Ticker(models.Model):
	ticker_symbol = models.CharField(max_length=5, verbose_name='symbol')
	exchange_symbol = models.CharField(max_length=10, verbose_name='exchange')
	instrument_id = models.IntegerField(default=0)
	num_followers = models.IntegerField(default=0, verbose_name='followers')
	earnings_announcement = models.DateField(null=True, blank=True, verbose_name='earnings date')
	percent_change_historical = models.DecimalField(max_digits=11, decimal_places=3, verbose_name='% change 50d')
	company_name = models.CharField(max_length=120, null=True, blank=True, verbose_name='name')

	def __unicode__(self):
		return self.ticker_symbol

	class Meta:
		ordering = ['ticker_symbol'] 

	def scorecards(self):
		""" how many scorecards have this ticker? """

		# find the ServiceTakes that have this ticker as a foreign key
		service_takes_on_this_ticker = ServiceTake.objects.filter(ticker=self)

		# of those, find the number of unique scorecards. use set() to avoid
		# counting cases where a scorecard has rec'd a ticker more than once
		scorecards_represented = set()
		for service_take in service_takes_on_this_ticker:
			scorecards_represented.add(service_take.scorecard.name)

		return len(scorecards_represented)

	def services(self):
		""" how many services have this ticker? """

		# find the ServiceTakes that have this ticker as a foreign key
		service_takes_on_this_ticker = ServiceTake.objects.filter(ticker=self)

		# of those, find the number of unique services. use set() so that if
		# a service has multiple scorecards (eg supernova & stock advisor),
		# we don't inflate the count
		services_represented = set()
		for service_take in service_takes_on_this_ticker:
			services_represented.add(service_take.scorecard.service.name)

		return len(services_represented)


class Service(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['name'] 


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
	date_pub = models.DateField(null=True, blank=True)
	url = models.URLField(max_length=400)
	service = models.ForeignKey(Service)
	ticker = models.ForeignKey(Ticker)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['-date_pub'] 