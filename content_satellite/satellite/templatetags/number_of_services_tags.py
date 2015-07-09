from django import template
from satellite.models import Ticker

register = template.Library()

@register.simple_tag
def get_number_of_services(ticker_symbol):
    """
    Given a ticker, find the number of services that cover it. 
    """
    try:
        number_of_services = Ticker.services(ticker_symbol)
        return number_of_services
    except:
        return None

@register.assignment_tag
def get_number_of_services(ticker_symbol):
    """
    Given a ticker, find the number of services that cover it. 
    """
    try:
        number_of_services = Ticker.services(ticker_symbol)
        return number_of_services
    except:
        return None