def _get_as_table(labels, data, is_percentages):
    rows = []

    top_row = '<tr style="border-bottom:1px dotted gray">' + ''.join(['<td width="70">%s</td>' % l for l in labels]) + '</tr>'

    if is_percentages:
        bottom_row = '<tr >' + ''.join(['<td>%.2f%%</td>' % d for d in data]) + '</tr>'
    else:
        bottom_row = '<tr>' + ''.join(['<td>$%.0f</td>' % d for d in data]) + '</tr>'

    markup = "<table style='background-color:yellow'>" + top_row + bottom_row + "</table>"

    return markup


# all functions return 2 elements: None|True|False, and descriptive string
def geopolitical_risk(ticker_profile):

    is_in_united_states = ticker_profile.hq_country=='United States'

    tokens = []
    if ticker_profile.hq_city:
        tokens.append(ticker_profile.hq_city)
    if ticker_profile.hq_state:
        tokens.append(ticker_profile.hq_state)
    if not is_in_united_states and ticker_profile.hq_country:
        tokens.append(ticker_profile.hq_country)

    location = ', '.join(tokens)
    if location:
        location = "HQ: "+ location
    if is_in_united_states:
        return True, location
    return None, location


def market_cap_over_half_billion(ticker_profile):
    if ticker_profile.market_cap == 0:
        return None, None

    is_bigger = ticker_profile.market_cap > 500
    return is_bigger, "market cap: $%.0f M" % int(ticker_profile.market_cap)


def market_cap_over_one_billion(ticker_profile):

    if ticker_profile.market_cap == 0:
        return None, None
    is_bigger = ticker_profile.market_cap > 1000
    return is_bigger, "market cap: $%.0f M" % int(ticker_profile.market_cap)


def profitable_ltm(ticker_profile):
    if ticker_profile.net_income_ltm == 0:
        return None, None
    is_bigger = ticker_profile.net_income_ltm > 0
    return is_bigger, 'net income LTM: $%.0f' % ticker_profile.net_income_ltm

def operating_cash_flow_positive_ltm_and_mrq(ticker_profile):
    if ticker_profile.operating_cash_ltm == 0 or ticker_profile.operating_cash_mrq == 0:
        return None, None
    is_positive = ticker_profile.operating_cash_ltm > 0 and ticker_profile.operating_cash_mrq > 0

    return is_positive, 'operating cash flow LTM: $%.0f, MRQ: $%.0f' % (ticker_profile.operating_cash_ltm, ticker_profile.operating_cash_mrq)


def profitable_ltm_and_mrq(ticker_profile):
    if ticker_profile.net_income_ltm == 0 or ticker_profile.net_income_mrq == 0:
        return None, None
    is_positive = ticker_profile.net_income_ltm > 0 and ticker_profile.net_income_mrq > 0

    return is_positive, 'net income LTM: $%.0f, MRQ: $%.0f' % (ticker_profile.net_income_ltm, ticker_profile.net_income_mrq)


def free_cash_flow_positive_two_of_three_years(ticker_profile):
    fcf = ticker_profile.get_free_cash_flow_Last_3_years()

    positive_years = 0
    description_tokens = []
    labels = ['LTM', '-1', '-2', '-3']
    for i in range(0, len(fcf)-1):
        if fcf[i] > 0:
            positive_years += 1

    description = _get_as_table(labels, fcf, False)
    print description, '!!!'
    return positive_years>=2, description

def profitable_last_five_years(ticker_profile):

    net_income_last_five_years = ticker_profile.get_net_income_last_five_years()

    had_a_loss = False
    description_tokens = []
    labels = ['LTM', '-1', '-2', '-3', '-4', '-5']
    for i in range(0, len(net_income_last_five_years)-1):
        if net_income_last_five_years[i] < 0:
            had_a_loss = True

    description = _get_as_table(labels, net_income_last_five_years, False)

    return not had_a_loss,description

def independence(ticker_profile):

    return None, "market cap: $%.0f; debt: $%.0f; cash: $%.0f" % (ticker_profile.market_cap, ticker_profile.total_debt, ticker_profile.cash_incl_st_investments)

def return_on_equity_over_twelve_percent_last_five_years(ticker_profile):
    roe_last_five_years = ticker_profile.get_roe_last_five_years()

    always_over_twelve_percent = True
    labels = ['LTM', '-1', '-2', '-3', '-4', '-5']
    for i in range(0, len(roe_last_five_years)):
        if roe_last_five_years[i]<12:
            always_over_twelve_percent = False

    description = _get_as_table(labels, roe_last_five_years, True)

    return not always_over_twelve_percent, description

def return_on_equity_over_fifteen_percent_last_year(ticker_profile):
    is_enough = ticker_profile.roe_ltm > 15
    return is_enough, 'ROE last year: %.2f%%' % ticker_profile.roe_ltm

def founders_have_stake(ticker_profile):
    insider_holdings_sum = ticker_profile.get_insider_holdings_sum()
    if insider_holdings_sum < 0:
        return None, None
    is_enough = insider_holdings_sum > 5.0
    return is_enough, 'insider holdings: %.2f%%' % insider_holdings_sum

def cagr_between_10_and_40_percent(ticker_profile):
      is_enough = ticker_profile.compound_annual_growth_rate_3_year >=10 and ticker_profile.compound_annual_growth_rate_3_year <= 40
      return is_enough, '3-year CAGR: %.2f%%' % ticker_profile.compound_annual_growth_rate_3_year

def beta_under_one_point_three(ticker_profile):
      is_small = ticker_profile.beta_ltm < 1.3
      return is_small, 'beta: %.2f' % ticker_profile.beta_ltm

def price_per_earnings_under_30(ticker_profile):
      is_small = ticker_profile.price_per_earnings < 30
      return is_small, 'p/e: %.1f; price: $%.2f; EPS: $%.2f' % (ticker_profile.price_per_earnings, ticker_profile.stock_price, ticker_profile.earnings_per_share)

def stock_advisor_savvy(ticker_profile):
      return None, "ROE: %.2f%%; debt: $%.0f; cash: $%.0f" % (ticker_profile.roe_ltm, ticker_profile.total_debt, ticker_profile.cash_incl_st_investments)

def debt_to_equity_under_40_percent(ticker_profile):
    is_under = ticker_profile.debt_to_equity < 40
    return is_under, "debt-to-equity: %.0f%%" % ticker_profile.debt_to_equity

def pro_social_company(ticker_profile):
    ps_ids = [206054, 205374, 207668, 288540, 203768, 224257, 273426, 203178, 203143, 202686]
    is_on_social = ticker_profile.ticker.instrument_id in ps_ids

    if is_on_social:
        return True, '%s is on our pro-social list!' % ticker_profile.ticker.company_name
    else:
        return None, None

def competitors(ticker_profile):
    return None, ticker_profile.competitors

def default_negative(ticker_profile):
    return False, None

def default_positive(ticker_profile):
    return True, None

def default_unknown(ticker_profile):
    return None, None
