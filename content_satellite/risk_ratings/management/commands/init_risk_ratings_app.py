from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):

    def handle(self, *args, **options):
    	print 'starting script'
        call_command('migrate')
        call_command('import_questions')
        call_command('import_tickers')
        call_command('sync_capiq_stats')
        call_command('sync_competitors')
    	print 'finished script'
