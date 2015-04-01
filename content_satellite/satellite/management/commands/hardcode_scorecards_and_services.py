from django.core.management.base import BaseCommand, CommandError

from satellite.models import Scorecard, Service

scorecards_by_service = {
	"supernova":["IB-Supernova-Odyssey","IB-Supernova-Phoenix","@SupernovaExplorer1Inclusion","IB-Supernova-Phoenix-2","@SupernovaExplorer2Inclusion","IB-Supernova-Explorer","IB-Supernova-ExplorerII"],
	"mdp_deep_value":["Schwab-Deep-Value",],
	"hidden_gems":['Schwab-Hidden-Gems',"@HiddenGemsInclusion",],
	'special_ops':['Schwab-Special-Ops',],
	'million_dollar_portfolio':['Schwab-MDP-Charter',],
	'one':['IB-Everlasting'],
	'stock_advisor':["@StockAdvisorDavidInclusion","@StockAdvisorTomInclusion",],
	'rule_breakers':['@RuleBreakersInclusion',],
	'income_investor':['@IncomeInvestorInclusion',],
	'inside_value':['@InsideValueInclusion',],
}

class Command(BaseCommand):
    help = "Inserts records for services and scorecards."

    def handle(self, *args, **options):
	    
		for service in scorecards_by_service.keys():
			s = Service()
			s.name = service
			s.save()

			for scorecard in scorecards_by_service[service]:
				sc = Scorecard()
				sc.service = s 
				sc.name = scorecard 
				sc.pretty_name = scorecard.replace("@","").replace("IB-","").replace("Inclusion","").replace("Schwab-","")
				sc.save()

		self.stdout.write("finished")
