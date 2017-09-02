leagues = []
id_to_index_map = {}
preffered_teams = []



class date:
	def __init__(self):
		self.year = '2000'
		self.month = '01'
		self.day = '01'

	def __str__(self):
		return self.year + '-' + self.month + '-' + self.day

	def getDay(self):
		return self.day

	def getMonth(self):
		return self.month

	def getYear(self):
		return self.year



class time:
	def __init__(self):
		self.hour = '00'
		self.minutes = '00'
		self.seconds = '00'

	def __str__(self):
		return self.hour + ':' + self.minutes + ':' + self.seconds

	def getHour(self):
		return self.hour

	def getMinutes(self):
		return self.minutes

	def getSeconds(self):
		return self.seconds

	def showTime(self):
		return __str__(self)

	def showLocalTime(self, time_t):
		localTime = time()
		localTime.hour = str(int(self.hour) + int(time_t.hour))
		localTime.minutes = str(int(self.minutes) + int(time_t.minutes))
		localTime.seconds = str(int(self.seconds) + int(time_t.seconds))
		return localTime.showTime(self)






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
		self.fixtureId = ''
		self.leagueId = ''
		self.date = date()
		self.time = time()
		self.homeTeam = team()
		self.awayTeam = team()
		self.gameStatus = ''
		self.goalsHomeTeam = 0
		self.goalsAwayTeam = 0
		self.goalsAwayTeamHalfTime = 0
		self.goalsHomeTeamsHalfTime = 0
		self.minutesPlayed = 0

	def __str__(self):
		txt = self.awayTeam.name + ' vs ' + self.homeTeam.name
		return txt

	def getDate(self):
		return self.date

	def getStatus(self):
		return self.gameStatus

	def getHomeTeamName(self):
		return self.homeTeam.name


	def getAwayTeamName(self):
		return self.awayTeam.name

	def getScoreLine(self):
		return self.awayTeam.shortName + '   ' + str(self.goalsAwayTeam) + ' - ' + str(self.goalsHomeTeam) + '   ' + self.homeTeam.shortName


	def getResult(self):
		txt = str(self.minutesPlayed) + '\n' + self.getScoreLine()
		return txt

	def getId(self):
		return self.fixtureId





def findTeamCode(teamName, leagueId):
	league_l = leagues[id_to_index_map[leagueId]]
	for team_t in league_l.teams:
		if team_t.name == teamName:
			return team_t.codeName