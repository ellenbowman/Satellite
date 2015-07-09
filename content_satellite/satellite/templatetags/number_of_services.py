from django import template
from satellite.models import Ticker

register = template.Library()

@register.simple_tag
def get_number_of_services(ticker):
    """
    Given a ticker, find the number of services that cover it. 
    """
    ticker = Ticker.objects.filter(ticker=ticker)
    print ticker

    if ticker:
        number_of_services = Ticker.services(ticker)
        return number_of_services