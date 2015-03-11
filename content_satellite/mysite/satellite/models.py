from django.db import models

class Ticker(models.Model):
	ticker_symbol = models.CharField(max_length=5)
	exchange_symbol = models.CharField(max_length=10)
	instrument_id = models.IntegerField(default=0)
	num_followers = models.IntegerField(default=0)
	earnings_announcement = models.DateField(null=True, blank=True)
	percent_change_historical = models.DecimalField(max_digits=11, decimal_places=5)
	company_name = models.CharField(max_length=120, null=True, blank=True)
	def __unicode__(self):
		return self.ticker_symbol

class Service(models.Model):
	name = models.CharField(max_length=20)
	def __unicode__(self):
		return self.name

class Scorecard(models.Model):
	name = models.CharField(max_length=30)
	service = models.ForeignKey(Service)
	pretty_name = models.CharField(max_length=30)
	def __unicode__(self):
		return self.pretty_name

class ServiceTake(models.Model):
	is_first = models.BooleanField(default=False)
	is_newest= models.BooleanField(default=False)
	action = models.CharField(max_length=10)
	is_core = models.BooleanField(default=False)
	is_present = models.BooleanField(default=False)
	ticker = models.ForeignKey(Ticker)
	scorecard = models.ForeignKey(Scorecard)
	def __unicode__(self):
		return str(self.ticker) + " " + str(self.scorecard)

class Article(models.Model):
	title = models.CharField(max_length=100)
	author = models.CharField(max_length=50)
	date_pub = models.DateField(null=True, blank=True)
	url = models.URLField(max_length=400)
	service = models.ForeignKey(Service)
	ticker = models.ForeignKey(Ticker)
	def __unicode__(self):
		return self.title