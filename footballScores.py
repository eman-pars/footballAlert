import sys, json
import http.client
import urllib
import urllib.request as ur

#from footballScores 
from class_implementn import *
import alert_implementn as alert_



api_key = sys.argv[1]
data_URL = "http://api.football-data.org"

preffered_leaguesID = [445, ]

#
# class to store a fixture





def StrToDateTime(dateTimeString):
	dateTime = dateTimeString.split('Z')[0]
	dateTime = dateTime.split('T')
	return dateTime


def StrToDate(dateString):
	listDate = dateString.split('-')
	return listDate

def StrToTime(timeString):
	listTime = timeString.split(':')
	return listTime


def createDateFromListDate(listDate):
	date_d = date()
	date_d.year = listDate[0]
	date_d.month = listDate[1]
	date_d.day = listDate[2]
	return date_d

def createTimeFromLisrTime(listTime):
	time_t = time()
	time_t.hour = listTime[0]
	time_t.minutes = listTime[1]
	time_t.seconds = listTime[2]
	return time_t


def getDateObj(dateTimeString):
	dateStr = StrToDateTime(dateTimeString)
	dateStr = StrToDate(dateStr[0])
	return createDateFromListDate(dateStr)


def getTimeObj(dateTimeString):
	timeStr = StrToDateTime(dateTimeString)
	timeStr = StrToTime(timeStr[1])
	return createTimeFromLisrTime(timeStr)



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



def createTeamByIdLink(teamId):
	team_URL = '/v1/teams/' + str(teamId)
	json_data = getJsonData(team_URL)
	return createTeamByObj(json_data)

def createTeamByObj(obj):
	team_t = team()
	print(obj)
	team_t.name = obj['name']
	team_t.shortName = obj['shortName']
	return team_t






def createLeagueFixture(obj, leagueId):
	f_obj = fixture()
	f_obj.date = getDateObj(obj['date'])
	f_obj.time = getTimeObj(obj['date'])
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
	f_obj.date = getDateObj(obj['date'])
	f_obj.leagueId = obj['competitionId']
	f_obj.fixtureId = obj['id']
	f_obj.time = getTimeObj(obj['date'])
	f_obj.awayTeam = createTeamByIdLink(obj['awayTeamId'])
	f_obj.homeTeam = createTeamByIdLink(obj['homeTeamId'])
	f_obj.gameStatus = obj['status']
	f_obj.goalsAwayTeam = obj['result']['goalsAwayTeam']
	f_obj.goalsHomeTeam = obj['result']['goalsHomeTeam']
	return f_obj


def createLeagueFixtures(jsonData, leagueId):
	fixtures = []
	for obj in jsonData:
		f_obj = createFixture(obj)
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
	printFixtures(fixturesTempList)




def printFixtures(fixturesList):
	if fixturesList == []:
		print('No fixtures in this time frame!')
	else:
		for fixture_f in fixturesList:
			print(fixture_f)
		print('alert')
		alert_.writeScoreLine(fixturesList[0])




def getTimeFrameFilter(timeFrameArg):
	filterTimeFrame = ''
	if timeFrameArg == 0:
		timeFrameArg = 1;
	elif timeFrameArg < 0:
		filterTimeFrame = 'p' + str(-timeFrameArg)
	else:
		filterTimeFrame = 'n' + str(timeFrameArg)

	return filterTimeFrame



def showLeagueFixtures(timeFrame ,leagueId):
	fixturesTempList = getLeagueFixtures(timeFrame, leagueId)
	printFixtures(fixturesTempList)



def getFixturesToday():
	return getFixtures(1)



def getLeagueFixtures(timeFrame, leagueId):
	filterTimeFrame = getTimeFrameFilter(timeFrame)
	leagueFixtures_URL = '/v1/competitions/' + str(leagueId) + '/fixtures?timeFrame=' + filterTimeFrame
	print(leagueFixtures_URL)
	json_data = getJsonData(leagueFixtures_URL)
	leagueFixtures = createLeagueFixtures(json_data['fixtures'], leagueId)
	return leagueFixtures



def getFixtures(timeFrame):
	filterTimeFrame = getTimeFrameFilter(timeFrame)
	fixtures_URL = '/v1/fixtures?timeFrame=' + filterTimeFrame
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
	showLeagueFixtures(8, 445)


	
	
