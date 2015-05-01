from datetime import datetime, timedelta
from django.core.management import call_command
from django.shortcuts import redirect, render
from django.http import HttpResponse
from models import DataHarvestEventLog, DATA_HARVEST_TYPE_CHOICES

def data_freshness_index(request):
	
	recent_events_overall = DataHarvestEventLog.objects.all().order_by('-date_started')[:50]

	most_recent_event_per_type = []
	
	for ht in DATA_HARVEST_TYPE_CHOICES:
		ht_id = ht[0]
		ht_pretty_name = ht[1]

		events_for_this_type = DataHarvestEventLog.objects.filter(data_type=ht_id).order_by('-date_started')
		date_of_most_recent_event_of_this_type = None
		if events_for_this_type:
			date_of_most_recent_event_of_this_type = events_for_this_type[0].date_started

		most_recent_event_per_type.append({
			'pretty_name':ht_pretty_name, 
			'type':ht_id, 
			'date':date_of_most_recent_event_of_this_type
			})

	dictionary_of_values = {
		'recent_events':recent_events_overall,
		'most_recent_event_per_type':most_recent_event_per_type
	}

	return render(request, 'satellite/data_freshness_index.html', dictionary_of_values)
