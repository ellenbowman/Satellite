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
        author = [a.author for a in preselected_authors]
    return author

@register.assignment_tag
def get_author_name(coverage_choice_id, ticker):
    """
    Given a ticker and the integer representation of a coverage choice,
    find all CoverageType records, and from that set compile the author names
    """
    coverage_pledges = CoverageType.objects.filter(ticker=ticker, coverage_type=coverage_choice_id)
    return [cp.author for cp in coverage_pledges]