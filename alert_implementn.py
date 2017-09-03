import subprocess,sys
from class_implementn import fixture, league, date, time, team
from crontab import CronTab

def notifyFixture(fixture_f):
	title = fixture_f.awayTeam.shortName + ' vs ' + fixture_f.homeTeam.shortName
	msg = str(fixture_f.date) + "   |   " + fixture_f.time.shortTime(fixture_f.time.showISTTime())
	msg = msg + "\nStatus: " + fixture_f.gameStatus
	notify(title, msg, 1000)


def notifyLeagueFixtures(fixturesList, timeFrame, leagueId):
	if timeFrame < 0:
		title = 'League Fixtures, prev ' + str(timeFrame) + ' Days'
	else:
		title = 'League Fixtures, next ' + str(timeFrame) + ' Days'
	
	msg = ''

	if fixturesList == []:
		msg = 'No Fixtures in this time frame!'
	else:
		for fixture_f in fixturesList:
			msg += str(fixture_f)
			msg += '\n'
	notify(title, msg, 5000)



def notifyFixtures(fixturesList, timeFrame):
	if timeFrame < 0:
		title = 'Fixtures, prev ' + str(timeFrame) + ' Days'
	else:
		title = 'Fixtures, next ' + str(timeFrame) + ' Days'
	
	msg = ''

	if fixturesList == []:
		msg = 'No Fixtures in this time frame!'
	else:
		for fixture_f in fixturesList:
			msg += str(fixture_f)
	notify(title, msg, 5000)




def notifyScoreLine(fixture_f):
	title = str(fixture_f)
	msg = fixture_f.getScoreLine()
	msg = msg + '\n' + str(fixture_f.minutesPlayed) + "'"
	notify(title, msg, 3000)


def notify(title, msg, timeout):
	expireTime = '--expire-time=' + str(timeout)
	subprocess.Popen(['notify-send', expireTime, '--urgency=critical' , title, msg])




# cron = CronTab(user=sys.argv[3])
# leagueFixtureCheck = cron.command('')




	