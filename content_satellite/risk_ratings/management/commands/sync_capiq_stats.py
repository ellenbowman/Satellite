import os
import xlrd
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from risk_ratings.models import Ticker, TickerProfile, DataImportLog

CAP_IQ_WORKBOOK = 'risk_ratings\\data\\capIq\\stats.xls'

PROFILES_SHEET_NAME = 'profiles'
FIGURES_SHEET_NAME = 'figures'
HOLDINGS_SHEET_NAME = 'insider holdings'

PROFILE_COLUMNS = ['','IQ_CITY','IQ_STATE','IQ_COUNTRY_NAME','IQ_COMPANY_NAME','IQ_CEO_NAME','IQ_EST_NEXT_EARNINGS_DATE']
FIGURES_COLUMNS = ['','Profitability LTM','Profitability year-1','Profitability year-2','Profitability year-3',
'Profitability year-4','Profitability yea-5','Profitability MRQ','Free Cash Flow LTM','Free Cash Flow y-1',
'Free Cash Flow y-2','Free Cash Flow Y-3','Cash flow LTM','Cash flow MRQ','Growth 3yr CAGR','Market Cap','Debt',
'Debt-to-equity','Cash (includes ST investments)','ROE LTM','ROE y-1','ROE y-2','ROE y-3','ROE y-4','ROE y-5',
'BETA LTM','STOCK PRICE','Earnings per share','price per earnings']
HOLDINGS_COLUMNS = ['', '', '', '', '', '', '']

SHEETS= {
    PROFILES_SHEET_NAME: PROFILE_COLUMNS,
    FIGURES_SHEET_NAME: FIGURES_COLUMNS,
    HOLDINGS_SHEET_NAME: HOLDINGS_COLUMNS
}

def is_row_valid(tokens, SHEET_NAME):
    if '(Capability Needed)' in tokens or '(Invalid Identifier)' in tokens:
        print 'bad data %s' % str(tokens)[:50]
        return False

    if len(tokens) != len(SHEETS[SHEET_NAME]):
        print 'wrong length %s' % str(tokens)[:50]
        return False

    return True


def sanitize_tokens(tokens):

    clean_tokens = []
    for t in tokens:

        # process strings
        if t is not None and hasattr(t, 'strip'):
            t = t.strip()

            if t.startswith('"') and t.endswith('"'):
                t = t[1:-1].strip()

            elif t == '$-':
                t = '0'

            else:
                t = t.replace('$','').replace(',','').replace('"','').strip()

                if t.startswith('(') and t.endswith(')'):
                    try:
                        # negative integer
                        t = int(t[1:-1])
                        t *= -1
                    except:
                        pass

            try:
                t = t.decode('iso-8859-1').encode('ascii', 'replace')
            except:
                pass

        clean_tokens.append(t)

    return clean_tokens

def get_ticker_stats_for_symbol(ticker_symbol):
    ticker_symbol = ticker_symbol.replace('.','-').strip() # eg BRK-B (TMF) --> BRK.B (CapIQ)

    try:
        ticker = Ticker.objects.get(symbol=ticker_symbol)
    except:
        print 'no Ticker for %s' % ticker_symbol
        return None

    try:
        tickerStats = TickerProfile.objects.get(ticker=ticker)
    except:
        tickerStats = TickerProfile.objects.create(ticker=ticker)

    return tickerStats

class Command(BaseCommand):

    def handle(self, *args, **options):
    	print 'starting script'

        script_start_time = datetime.now()

        workbook_file = CAP_IQ_WORKBOOK

        print 'looking for workbook', workbook_file

        workbook = xlrd.open_workbook(workbook_file)

        # validate sheets & columns fit our expectations
        expected_sheet_names = SHEETS.keys()
        if set(expected_sheet_names) & set(workbook.sheet_names()) != set(expected_sheet_names):
            print 'did not detect all expected sheets'
            print workbook.sheet_names()
            raise

        for sheet_name in SHEETS:
            sheet = workbook.sheet_by_name(sheet_name)
            if sheet.row_values(0) != SHEETS[sheet_name]:
                print 'mismatch in columns: ' + sheet_name
                raise

        ################################################
        profiles_sheet = workbook.sheet_by_name(PROFILES_SHEET_NAME)
        for i in range(1, profiles_sheet.nrows):
            tokens = profiles_sheet.row_values(i)

            if not is_row_valid(tokens,PROFILES_SHEET_NAME):
                continue

            tokens = sanitize_tokens(tokens)

            ticker_symbol = tokens[0]
            tickerStats = get_ticker_stats_for_symbol(ticker_symbol)
            if not tickerStats:
                continue

            tickerStats.hq_city = tokens[1] if tokens[1] is not 0 else None
            tickerStats.hq_state = tokens[2] if tokens[2] is not 0 else None
            tickerStats.hq_country = tokens[3] if tokens[3] is not 0 else None

            try:
                tickerStats.save()
            except Exception as e:
                print e
                print tokens
                raise

        print 'finished saving profiles'

        #############################
        figures_sheet = workbook.sheet_by_name(FIGURES_SHEET_NAME)

        for i in range(1, figures_sheet.nrows):
            tokens = figures_sheet.row_values(i)

            if not is_row_valid(tokens, FIGURES_SHEET_NAME):
                continue

            tokens = sanitize_tokens(tokens)
            tokens = [0 if t=='NM' else t for t in tokens]

            ticker_symbol = tokens[0]
            tickerStats = get_ticker_stats_for_symbol(ticker_symbol)
            if not tickerStats:
                continue

            tickerStats.net_income_ltm = tokens[1]
            tickerStats.net_income_years_ago_1 = tokens[2]
            tickerStats.net_income_years_ago_2 = tokens[3]
            tickerStats.net_income_years_ago_3 = tokens[4]
            tickerStats.net_income_years_ago_4 = tokens[5]
            tickerStats.net_income_years_ago_5 = tokens[6]
            tickerStats.net_income_mrq = tokens[7]

            tickerStats.free_cash_flow_ltm = tokens[8]
            tickerStats.free_cash_flow_years_ago_1 = tokens[9]
            tickerStats.free_cash_flow_years_ago_2 = tokens[10]
            tickerStats.free_cash_flow_years_ago_3 = tokens[11]

            tickerStats.operating_cash_ltm = tokens[12]
            tickerStats.operating_cash_mrq = tokens[13]

            tickerStats.compound_annual_growth_rate_3_year = tokens[14]

            tickerStats.market_cap = tokens[15]
            tickerStats.total_debt = tokens[16]
            tickerStats.debt_to_equity = tokens[17]
            tickerStats.cash_incl_st_investments = tokens[18]

            tickerStats.roe_ltm = tokens[19]
            tickerStats.roe_years_ago_1 = tokens[20]
            tickerStats.roe_years_ago_2 = tokens[21]
            tickerStats.roe_years_ago_3 = tokens[22]
            tickerStats.roe_years_ago_4 = tokens[23]
            tickerStats.roe_years_ago_5  = tokens[24]

            tickerStats.beta_ltm = tokens[25]
            tickerStats.stock_price = tokens[26]
            tickerStats.earnings_per_share = tokens[27]
            tickerStats.price_per_earnings = tokens[28] if tokens[28]!='#DIV/0!' else 0

            try:
                tickerStats.save()
            except Exception as e:
                print e
                print tokens
                raise

        print 'finished saving figures'
        #############################

        holdings_sheet = workbook.sheet_by_name(HOLDINGS_SHEET_NAME)
        for i in range(1, holdings_sheet.nrows):
            tokens = holdings_sheet.row_values(i)

            if not is_row_valid(tokens,HOLDINGS_SHEET_NAME):
                continue

            tokens = sanitize_tokens(tokens)

            ticker_symbol = tokens[0]
            tickerStats = get_ticker_stats_for_symbol(ticker_symbol)
            if not tickerStats:
                continue

            if tokens[1] != 0:
                tickerStats.insider_holdings_1 = tokens[1]
                tickerStats.insider_holdings_2 = tokens[2]
                tickerStats.insider_holdings_3 = tokens[3]
                tickerStats.insider_holdings_4 = tokens[4]
                tickerStats.insider_holdings_5 = tokens[5]
            else:
                tickerStats.insider_holdings_1 = -1
                tickerStats.insider_holdings_2 = -1
                tickerStats.insider_holdings_3 = -1
                tickerStats.insider_holdings_4 = -1
                tickerStats.insider_holdings_5 = -1

            try:
                tickerStats.save()
            except Exception as e:
                print e
                print tokens
                raise
        print 'finished saving holdings'


        DataImportLog.objects.create(ticker_count=figures_sheet.nrows-1)

    	print 'finished script'
        print 'ticker profiles:', TickerProfile.objects.count()

        seconds_elapsed = (datetime.now() - script_start_time).total_seconds()
        print 'total seconds:', seconds_elapsed
