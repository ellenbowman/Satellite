from django import template
from satellite.models import CoverageType

register = template.Library()

@register.simple_tag
def get_service_pledges(ticker, coverage_choice_id):
    """
    Given a ticker and the integer representation of a coverage choice,
    find all CoverageType records, and from that set compile a string of the pretty names of the associated services
    """
    coverage_pledges = CoverageType.objects.filter(ticker=ticker, coverage_type=coverage_choice_id)

    if coverage_pledges:
        services = [cp.service.pretty_name for cp in coverage_pledges]
        return ', '.join(services)

    return ''


@register.assignment_tag
def get_services_ids(coverage_choice_id, ticker):
    """
    Given a ticker and the integer representation of a coverage choice,
    find all CoverageType records, adn from that set compile the ids of teh associated services
    """
    coverage_pledges = CoverageType.objects.filter(ticker=ticker, coverage_type=coverage_choice_id)
    return [cp.service.id for cp in coverage_pledges]
