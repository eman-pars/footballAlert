import sys, json
import http.client
import urllib
import urllib.request as ur
from bs4 import BeautifulSoup

api_key = sys.argv[1]
data_URL = "http://api.football-data.org"








# Code for not using the system proxy
# Create custom proxyHandler with no proxies

proxy = sys.argv[2]


proxy_handler = ur.ProxyHandler({'http' : proxy})
auth = urllib.request.HTTPBasicAuthHandler()
opener = ur.build_opener(proxy_handler, auth, urllib.request.HTTPHandler)
ur.install_opener(opener)






# Craft a request to the API
# Create a http connection, obtain response
#

# 
# connection.set_tunnel(data_URL)
# headers = {'X-Auth-Token':api_key, 'X-Response-Control':'minified'}
# connection.request('GET', '/v1/competitions/445/fixtures', None, headers)
# response = connection.getresponse()
# data = response.read().decode()
# print(data)
# json_data = json.loads(data)
# fixtures = json_data['fixtures']
# for obj in fixtures:
# 	txt = fixtures['homeTeamName'] + 'vs' + fixtures['awayTeamName']
# 	print(txt)

page = ur.urlopen(data_URL + '/v1/competitions/445/fixtures')
print(page)


