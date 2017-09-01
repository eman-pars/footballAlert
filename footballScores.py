import sys, json, subprocess
import http.client
import urllib
import urllib.request as ur
from bs4 import BeautifulSoup

api_key = sys.argv[1]
data_URL = "http://api.football-data.org"
leagues = []
id_to_index_map = {}
preffered_teams = []
preffered_leaguesID = [445, ]

#
# class to store a fixture




class team:
	def __init__(self):
		self.name = ''
		self.shortName = ''
		self.codeName = ''
		self.id = 0
		self.leagueId = 0


	def __str__(self):
		return self.name

	def getTeamCode(self):
		return self.codeName

	def getShortName(self):
		return self.shortName

	def getId(self):
		return self.id

	def getLeague(self):
		return leagues[id_to_index_map[self.leagueId]].name



class league:
	def __init__(self):
		self.name = ''
		self.league = ''
		self.id = 0
		self.year = 0
		self.teamCount = 0
		self.totalMatchDays = 0
		self.currentMatchDays = 0
		self.totalFixtures = 0
		self.teams = []
		self.fixtures = []
		self.index = -1

	def __str__(self):
		return self.name

	def getName(self):
		return self.name

	def getTeamCount(self):
		return self.teamCount

	def listTeams(self):
		for team_t in self.teams:
			print(team_t.name)



class fixture:	
	def __init__(self):
		self.leagueId = ''
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
		if self.awayTeamCode == '':
			self.setAwayTeamCode()
		if self.homeTeamCode == '':
			self.setHomeTeamCode()

		return self.awayTeamCode + str(self.goalsAwayTeam) + ' - ' + str(self.goalsHomeTeam) + self.homeTeamCode

	def getResult(self):
		txt = str(self.minutes) + '\n' + self.getScoreLine()
		return txt

	def setAwayTeamCode():
		self.awayTeamCode = findTeamCode(self.awayTeamName, self.leagueId)

	def setHomeTeamCode():
		self.homeTeamCode = findTeamCode(self.homeTeamName, self.leagueId)




def getLeagues():
	leagues_URL = '/v1/competitions/'
	json_data = getJsonData(leagues_URL)

	for ctr, league_l in enumerate(json_data, start = 0):
		l_obj = league()
		l_obj.name = league_l['caption']
		l_obj.league = league_l['league']
		l_obj.id = league_l['id']
		l_obj.year = league_l['year']
		l_obj.currentMatchDays = league_l['currentMatchday']
		l_obj.totalMatchDays = league_l['numberOfMatchdays']
		l_obj.totalFixtures = league_l['numberOfGames']
		l_obj.teamCount = league_l['numberOfTeams']
		l_obj.teams = getTeams(l_obj.id)
		l_obj.index = ctr
		leagues.append(l_obj)
		id_to_index_map[l_obj.id] = l_obj.index





def getTeams(leagueId):
	leagueTeams_URL = '/v1/competitions/' + str(leagueId) + '/teams'
	json_data = getJsonData(leagueTeams_URL)

	teams_data = json_data['teams']

	teamsTemp = []
	for team_t in teams_data:
		t_obj = team()
		t_obj.name = team_t['name']
		t_obj.codeName = team_t['code']
		t_obj.shortName = team_t['shortName']
		teamsTemp.append(t_obj)

	return teamsTemp


	
def getLeagueFixtures(leagueId):
	league_l = leagues[id_to_index_map[leagueId]]
	leagueFixtures_URL = '/v1/competitions/' + str(leagueId) + '/fixtures'
	json_data = getJsonData(leagueFixtures_URL)


	fixtures_data = json_data['fixtures']
	
	league_l.fixtures.append(createFixtures(fixtures_data, leagueId))


def createFixture(obj, leagueId):
	f_obj = fixture()
	f_obj.date = obj['date']
	f_obj.awayTeamName = obj['awayTeamName']
	f_obj.homeTeamName = obj['homeTeamName']
	f_obj.gameStatus = obj['status']
	f_obj.goalsAwayTeam = obj['result']['goalsAwayTeam']
	f_obj.goalsHomeTeam = obj['result']['goalsHomeTeam']
	f_obj.leagueId = leagueId
	f_obj.awayTeamCode = findTeamCode(f_obj.awayTeamName, f_obj.leagueId)
	f_obj.homeTeamCode = findTeamCode(f_obj.homeTeamName, f_obj.leagueId)
	return f_obj


def createFixture(obj):
	f_obj = fixture()
	f_obj.date = obj['date']
	f_obj.awayTeamName = obj['awayTeamName']
	f_obj.homeTeamName = obj['homeTeamName']
	f_obj.gameStatus = obj['status']
	f_obj.goalsAwayTeam = obj['result']['goalsAwayTeam']
	f_obj.goalsHomeTeam = obj['result']['goalsHomeTeam']
	return f_obj


def createFixtures(jsonData, leagueId):
	fixtures = []
	for obj in jsonData:
		f_obj = createFixture(obj, leagueId)
		fixtures.append(f_obj)

	return fixtures


def createFixtures(jsonData):
	fixtures = []
	for obj in jsonData:
		f_obj = createFixture(obj)
		fixtures.append(f_obj)

	return fixtures



def getJsonData(URL):
	headers = {'X-Auth-Token': api_key, 'X-Response-Control':'minified'}
	#headers = headers.encode('ascii')
	req = ur.Request(data_URL + URL, headers = headers)
	page = ur.urlopen(req)
	data = page.read().decode('utf8')
	json_data = json.loads(data)
	return json_data



def findTeamCode(teamName, leagueId):
	league_l = leagues[id_to_index_map[leagueId]]
	for team_t in league_l.teams:
		if team_t.name == teamName:
			return team_t.codeName



def findLeagueName(leagueId):
	for league_l in leagues:
		if league_l.id == leagueId:
			return league_l.name


############################################################################################
# Query Funtions 


def showFixturedToday():
	fixturesToday = getFixturesToday()
	if fixturesToday == []:
		print('No fixtures today!!')
	else:
		for fixture_f in fixturesToday:
			print(fixture_f)


def showFixtures(timeFrame):
	fixturesTempList = getFixtures(timeFrame)
	if fixturesTempList == []:
		print('No fixtures in this time frame!')
	else:
		for fixture_f in fixturesTempList:
			print(fixture_f)


def getFixturesToday():
	return getFixtures(1)



def getFixtures(timeFrame):
	filterTimeFrame = ''
	if timeFrame == 0:
		timeFrame = 1;
	elif timeFrame < 0:
		filterTimeFrame = 'p' + str(-timeFrame)
	else:
		filterTimeFrame = 'n' + str(timeFrame)
	
	fixtures_URL = '/v1/fixtures?timeFrame=' + filterTimeFrame
	print(fixtures_URL)
	json_data = getJsonData(fixtures_URL)
	fixturesCount = json_data['count']
	fixturesTempList = createFixtures(json_data['fixtures'])
	return fixturesTempList


# Code for not using the system proxy
# Create custom proxyHandler with no proxies
def setProxy(argv_proxy):
	proxy = argv_proxy
	proxy_handler = ur.ProxyHandler({'http' : proxy})
	auth = urllib.request.HTTPBasicAuthHandler()
	opener = ur.build_opener(proxy_handler, auth, urllib.request.HTTPHandler)
	ur.install_opener(opener)




def writeNotify(title, msg):
	subprocess.Popen(['notify-send', title, msg])


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





if __name__ == '__main__':
	setProxy(sys.argv[2])
	showFixturedToday()
	showFixtures(4)
	print('--------------------------------------\n')
	showFixtures(-5)
	writeNotify('tielhdf','this is a msg')
	# getLeagues()
	# for league_l in leagues:
	# 	league_l.listTeams()
	
