import sys, json
import http.client
import urllib
import urllib.request as ur
from bs4 import BeautifulSoup

api_key = sys.argv[1]
data_URL = "http://api.football-data.org"
leagues = []


#
# class to store a fixture




class team:
	def __init__(self):
		self.name = ''
		self.shortName = ''
		self.codeName = ''
		self.id = 0


	def __str__(self):
		return self.name

	def getTeamCode(self):
		return self.codeName

	def getShortName(self):
		return self.shortName

	def getId(self):
		return self.id



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
		txt = findTeamCode(self.awayTeamName, self.leagueId) + ' ' + str(self.goalsAwayTeam) + ' - ' \
		+ str(self.goalsHomeTeam) + ' ' + findTeamCode(self.homeTeamName, self.leagueId)
		return txt

	def getResult(self):
		txt = str(self.minutes) + '\n' + self.getScoreLine()
		return txt




def getLeagues():
	leagues_URL = '/v1/competitions/'
	json_data = getJsonData(leagues_URL)

	for league_l in json_data:
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
		leagues.append(l_obj)




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


	





def getJsonData(URL):
	page = ur.urlopen(data_URL + URL)
	data = page.read().decode('utf8')
	json_data = json.loads(data)
	return json_data



def findTeamCode(teamName, leagueId):
	for league_l in leagues:
		if league_l.id == leagueId:
			for team_t in league_l.teams:
				if team_t.name == teamName:
					return team_t.codeName








# Code for not using the system proxy
# Create custom proxyHandler with no proxies
def setProxy(argv_proxy):
	proxy = argv_proxy
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

def getFixturesLeague(qLeagueName):
	
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



if __name__ == '__main__':
	setProxy(sys.argv[2])
	getLeagues()
	for league_l in leagues:
		league_l.listTeams()
	
