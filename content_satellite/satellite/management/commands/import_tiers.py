"""
reading tier data from a tab-delimited file and assigning it to Ticker objects

refs:
 management commmands:
 	https://docs.djangoproject.com/en/1.7/howto/custom-management-commands/
 reading text files programmatically:
	http://learnpythonthehardway.org/book/ex15.html (through ex17.html )
"""

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def handle(self, *args, **options):
    	
    	# open up the file and reference it as 'tiers_file'
    	with open('satellite\\management\\tiers.txt') as tiers_file:

    		# read all lines in the file
    		all_lines_in_file = tiers_file.readlines()

    		# process the lines, one-by-one. and we'll skip the first line, since it's not a data point
    		for line_in_file in all_lines_in_file[1:]:

    			# break down each line into the data elements, which we know are tab-delimited
    			tokens = line_in_file.split('\t')

    			# we expect there to be 4 data elements per row; disregard rows that don't satisfy this constraint
    			if len(tokens)==4:
    				ticker_symbol = tokens[1].strip()
    				status = tokens[3].strip()

    			print ticker_symbol, status	

    			# TODO : 
    			#   find the Ticker object that corresponds to this ticker symbol,
    			#   assign the tier status
    			#   save the Ticker object



