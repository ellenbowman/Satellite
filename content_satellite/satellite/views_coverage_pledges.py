from django.shortcuts import render
from models import Ticker, COVERAGE_CHOICES


def index(request):
    """
    For multiple tickers, show associated CoverageType records across multiple services
    We'll let template tags do the heavy lifting.
    """
    tickers = Ticker.objects.all().order_by('company_name')[:100]

    context = {
        'page-title': 'Coverage Pledges',
        'tickers': tickers,
        'coverage_types': COVERAGE_CHOICES
    }

    return render(request, 'satellite/coverage_pledges_index.html', context)