import sys, json
import http.client
import urllib
import urllib.request as ur
from bs4 import BeautifulSoup

api_key = sys.argv[1]
data_URL = "http://api.football-data.org"
leagues = []
id_to_index_map = {}


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
			self.setAwayTeamCode(self.awayTeamName, self.leagueId)
		if self.homeTeamCode == '':
			self.setHomeTeamCode(self.homeTeamName, self.leagueId)

		return self.awayTeamCode + str(self.goalsAwayTeam) + ' - ' + str(self.goalsHomeTeam) + self.homeTeamCode

	def getResult(self):
		txt = str(self.minutes) + '\n' + self.getScoreLine()
		return txt

	def setAwayTeamCode(self.awayTeamName, self.leagueId):
		self.awayTeamCode = findTeamCode(self.awayTeamName, self.leagueId)

	def setHomeTeamCode(self.homeTeamName, self.leagueId):
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

	for obj in fixtures_data:
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
		league_l.fixtures.append(f_obj)




def getJsonData(URL):
	page = ur.urlopen(data_URL + URL)
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
			return league_l.







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





if __name__ == '__main__':
	setProxy(sys.argv[2])
	getLeagues()
	for league_l in leagues:
		league_l.listTeams()
	
