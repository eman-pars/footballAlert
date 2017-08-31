import sys, json
import http.client
import urllib
import urllib.request as ur
from bs4 import BeautifulSoup

api_key = sys.argv[1]
data_URL = "http://api.football-data.org"


#
# class to store a fixture

teamCodes = {}

def getTeamCodes():
	return 'ss'



def getJsonData(URL):
	page = ur.urlopen(data_URL + URL)
	data = page.read().decode('utf8')
	json_data = json.loads(data)
	return json_data


class fixture:
	
	def __init__(self):
		self.date = ''
		self.awayTeamName = ''
		self.homeTeamName = ''
		self.gameStatus = ''
		self.goalsHomeTeam = 0
		self.goalsAwayTeam = 0
		self.goalsAwayTeamHalfTime = 0
		self.goalsHomeTeamsHalfTime = 0
		self.homeTeamCode = ''
		self.awayTeamCode = ''
		self.minutes = 0

	def __str__(self):
		txt = self.awayTeamName + ' vs ' + self.homeTeamName
		return txt

	def getDate(self):
		return self.date

	def getStatus(self):
		return self.gameStatus

	def getHomeTeamName(self):
		return self.homeTeamName


	def getAwayTeamName(self):
		return self.awayTeamName

	def getScoreLine(self):
		txt = str(self.awayTeamCode) + ' ' + str(self.goalsAwayTeam) + ' - ' + str(self.goalsHomeTeam) + ' ' + (self.homeTeamCode)
		return txt

	def getResult(self):
		txt = str(self.minutes) + '\n' + self.getScoreLine()
		return txt





fixtures = []










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

fixturesBPL_URL = '/v1/competitions/445/fixtures'

json_data = getJsonData(fixturesBPL_URL)


fixtures_data = json_data['fixtures']

for obj in fixtures_data:
	f_obj = fixture()
	f_obj.date = obj['date']
	f_obj.awayTeamName = obj['awayTeamName']
	f_obj.homeTeamName = obj['homeTeamName']
	f_obj.gameStatus = obj['status']
	f_obj.goalsAwayTeam = obj['result']['goalsAwayTeam']
	f_obj.goalsHomeTeam = obj['result']['goalsHomeTeam']

	print(f_obj)
	print(f_obj.getResult())
	print('\n')
	fixtures.append(f_obj)


# soup = BeautifulSoup(page, "lxml")
# print(soup.prettify())

# scoreTable = soup.find_all('div', id='events')
# print(scoreTable)
#print(scoreTable.decendents)
