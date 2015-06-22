from django import template
from satellite.models import CoverageType

register = template.Library()

@register.simple_tag
def get_preselected_author(ticker, coverage_choice_id):
    """
    Given a ticker and the integer representation of a coverage choice,
    find all CoverageType records, and from that set create a string of the author's name 
    """
    preselected_author = CoverageType.objects.filter(ticker=ticker, coverage_type=coverage_choice_id)
    print preselected_author

    if preselected_author:
        author = [a.author for a in preselected_author]
    return author

@register.assignment_tag
def get_author_name(coverage_choice_id, ticker, service):
    """
    Given a ticker, coverage choice (its integer representation), and a service,
    figure out whether there exists a CoverageType record. Note: we expect at most one
    record, given any combo of ticker, coverage choice, and service.
    If there is one, then return its author value.
    """
    try:
        coverage_pledge = CoverageType.objects.get(ticker=ticker, coverage_type=coverage_choice_id, service=service)
        return coverage_pledge.author
    except:
        return None