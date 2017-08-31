import sys, json
import http.client
import urllib.request as ur
from bs4 import BeautifulSoup

api_key = sys.argv[1]
data_URL = "api.football-data.org"








# Code for not using the system proxy
# Create custom proxyHandler with no proxies

# proxy_handler = ur.ProxyHandler({})
# opener = ur.build_opener(proxy_handler)
# ur.install_opener(opener)


# Craft a request to the API
# Create a http connection, obtain response
#

connection = http.client.HTTPConnection(data_URL)
headers = {'X-Auth-Token':api_key, 'X-Response-Control':'minified'}
connection.request('GET', '/v1/competitions/445/fixtures', None, headers)
response = connection.getresponse()
data = response.read().decode()
json_data = json.loads(data)

print(json_data['fixtures'][1])

# page = ur.urlopen(URL)


# soup = BeautifulSoup(page, "lxml")
# print(soup.prettify())

# scoreTable = soup.find_all('div', id='events')
# print(scoreTable)
#print(scoreTable.decendents)
