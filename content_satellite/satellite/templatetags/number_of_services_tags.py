from django import template
from satellite.models import Ticker

register = template.Library()

@register.assignment_tag
def get_number_of_services(ticker_symbol):
    """
    Given a ticker, find the number of services that cover it.
    """
    try:
        ticker = Ticker.objects.get(ticker_symbol = ticker_symbol)
        if ticker.services_for_ticker:
            return len(ticker.services_for_ticker.split(','))
        else:
            return 0
    except:
        return None
