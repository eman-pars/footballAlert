import subprocess
from class_implementn import fixture, league, date, time, team

def writeNotifyFixture(fixture_f):
	title = fixture_f.awayTeamName + ' vs ' + fixture_f.homeTeamName
	msg = str(fixture_f.date) + "   |   " + str(fixture_f.time)  
	msg = msg + "\nStatus: " + fixture_f.gameStatus
	print(msg)
	writeNotify(title, msg)


def writeScoreLine(fixture_f):
	title = str(fixture_f)
	msg = fixture_f.getScoreLine()
	writeNotify(title, msg)


def writeNotify(title, msg):
	subprocess.Popen(['notify-send','--expire-time=3000', '--urgency=critical' , title, msg])