url = "http://apiary.fool.com/PremiumScorecards/v1/scorecards/IB-Everlasting"
import urllib
response = urllib.urlopen(url)
read_response = response.read()
import json
json_response = json.loads(read_response)
#print json_response
op = json_response["OpenPositions"]
print len(op)
print op[0]