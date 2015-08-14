import json
from pytz import timezone
from django.db import models
from datetime import datetime

EASTERN_TZ = timezone('US/Eastern')

class Ticker(models.Model):

    symbol = models.CharField(max_length=10, blank=False)
    exchange = models.CharField(max_length=20, blank=False)
    company_name = models.CharField(max_length=200, blank=False)
    instrument_id = models.IntegerField()

    @staticmethod
    def get_as_list():
        all_tickers = Tickers.objects.all().order_by('symbol')
        return ["%s (%s)" % (t.symbol, t.company_name) for t in all_tickers]

    def __unicode__(self):
        return self.symbol


class TickerProfile(models.Model):

    ticker = models.ForeignKey(Ticker)

    hq_city = models.CharField(max_length=100, blank=True, null=True)
    hq_state = models.CharField(max_length=100, blank=True, null=True)
    hq_country = models.CharField(max_length=100, blank=True, null=True)

    year_founded = models.IntegerField(blank=True, null=True)

    ceo_name = models.CharField(max_length=100, blank=True, null=True)

    net_income_ltm = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_income_years_ago_1 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_income_years_ago_2 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_income_years_ago_3 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_income_years_ago_4 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_income_years_ago_5 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_income_mrq = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    free_cash_flow_ltm = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    free_cash_flow_years_ago_1 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    free_cash_flow_years_ago_2 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    free_cash_flow_years_ago_3 = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    operating_cash_ltm = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    operating_cash_mrq = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    compound_annual_growth_rate_3_year = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    market_cap = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    total_debt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    debt_to_equity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cash_incl_st_investments = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    roe_ltm = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    roe_years_ago_1 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    roe_years_ago_2 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    roe_years_ago_3 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    roe_years_ago_4 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    roe_years_ago_5 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    roe_mrq = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    beta_ltm = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    earnings_per_share = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price_per_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    insider_holdings_1 = models.DecimalField(max_digits=10, decimal_places=5, default=-1)
    insider_holdings_2 = models.DecimalField(max_digits=10, decimal_places=5, default=-1)
    insider_holdings_3 = models.DecimalField(max_digits=10, decimal_places=5, default=-1)
    insider_holdings_4 = models.DecimalField(max_digits=10, decimal_places=5, default=-1)
    insider_holdings_5 = models.DecimalField(max_digits=10, decimal_places=5, default=-1)

    competitors = models.CharField(max_length=500, null=True, blank=True)

    date_last_synced = models.DateTimeField()


    def save(self, *args, **kwargs):
        # update timestamps
        self.date_last_synced = datetime.now(EASTERN_TZ)
        return super(TickerProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.ticker.symbol

    def get_net_income_last_five_years(self):
        return [self.net_income_ltm, self.net_income_years_ago_1, self.net_income_years_ago_2,
        self.net_income_years_ago_3, self.net_income_years_ago_4, self.net_income_years_ago_5]

    def get_roe_last_five_years(self):
        return [self.roe_ltm, self.roe_years_ago_1, self.roe_years_ago_2,
        self.roe_years_ago_3, self.roe_years_ago_4, self.roe_years_ago_5]

    def get_insider_holdings(self):
        return [self.insider_holdings_1, self.insider_holdings_2, self.insider_holdings_3,
            self.insider_holdings_4, self.insider_holdings_5]

    def get_free_cash_flow_Last_3_years(self):
        return [self.free_cash_flow_ltm, self.free_cash_flow_years_ago_1, self.free_cash_flow_years_ago_2,
            self.free_cash_flow_years_ago_3]

    def get_insider_holdings_sum(self):
        # no data
        if self.insider_holdings_1 == -1:
            return -1

        return self.insider_holdings_1 + self.insider_holdings_2 + self.insider_holdings_3 + \
        self.insider_holdings_4 + self.insider_holdings_5


class Hint(models.Model):
    name = models.CharField(max_length=100, blank=False)
    function_name = models.CharField(max_length=100, blank=False)

    def __unicode__(self):
        return self.name


class Questionnaire(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def get_questions(self):
        questions = self.question_set.all().order_by('list_order')
        return questions

    def __unicode__(self):
        return self.name


class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire)
    label = models.CharField(max_length=100, blank=False)
    text = models.CharField(max_length=250, blank=False)
    list_order = models.IntegerField()

    hint = models.ForeignKey(Hint, null=True)

    def __unicode__(self):
        return "%d. %s: %s"  % (self.list_order, self.label, self.label)


class RiskRatingRecord(models.Model):
    legacy_uri = models.URLField()
    publish_date = models.DateField()
    headline = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    ticker = models.ForeignKey(Ticker)

    def get_full_url(self):
        base_url ='http://newsletters.fool.com'
        return base_url + self.legacy_uri

    def __unicode__(self):
        return "%s: %s"  % (self.ticker, self.publish_date.strftime('%Y-%m'))


CRUSHABILITY_CUTOFFS = [
    (2, 'Diamond'),
    (4, 'Black box'),
    (6, 'Carbon steel'),
    (8, 'Marble'),
    (10, 'Jawbreaker'),
    (12, 'Coconut'),
    (14, 'Glass Bottle'),
    (16, 'Soda can'),
    (18, 'Cardboard box'),
    (20, 'Beach ball'),
    (22, 'Egg'),
    (25, 'Peeps')
]

def get_crushability(count_negative_responses, max_points=25):

    if max_points != 25:
        # we introduce this shift, for convenience
        count_negative_responses += (25-max_points)

    for c in CRUSHABILITY_CUTOFFS:
        if count_negative_responses <= c[0]:
            return c[1]

    return CRUSHABILITY_CUTOFFS[-1][1]


class Feedback(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    comments = models.CharField(max_length=500)
    meta = models.CharField(max_length=500, blank=True, null=True)

    timestamp = models.DateTimeField()

    def save(self, *args, **kwargs):
        # update timestamps
        self.timestamp = datetime.now(EASTERN_TZ)
        return super(Feedback, self).save(*args, **kwargs)


class RiskRatingDraft(models.Model):

    questionnaire_name = models.CharField(max_length=50)
    ticker_symbol = models.CharField(max_length=10)
    responses_json = models.TextField()
    meta = models.CharField(max_length=100, blank=True, null=True)
    crushability_count = models.IntegerField()
    timestamp = models.DateTimeField()

    @property
    def crushability_label(self):
        return get_crushability(self.crushability_count)

    def save(self, *args, **kwargs):
        # update timestamps
        self.timestamp = datetime.now(EASTERN_TZ)
        return super(RiskRatingDraft, self).save(*args, **kwargs)


class DataImportLog(models.Model):
    ticker_count = models.IntegerField()
    timestamp = models.DateTimeField()

    @staticmethod
    def get_last_timestamp():
        if DataImportLog.objects.count():
            return DataImportLog.objects.all().order_by('-timestamp')[0].timestamp

        return None

    def save(self, *args, **kwargs):
        # update timestamps
        self.timestamp = datetime.now(EASTERN_TZ)
        return super(DataImportLog, self).save(*args, **kwargs)
