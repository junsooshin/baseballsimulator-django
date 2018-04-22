# List of methods in this module:
# 		- check_names()
# 		- get_correct_player()

# --------------------------------- Notes ----------------------------------- #
#
# Purpose: check_names method checks the batter and pitcher name strings
#          using the FanGraphs .csv files and returns invalid player names in a
#		   string list back to views.
#
# I am using the FanGraphs .csv files to check input because that's what I used
# to create objects and populate the database.
#
# To be a valid name:
#	it should exist in the .csv file AND not be a duplicate name
#	OR
#	it should be a duplicate-resolving string.
#
# --------------------------------------------------------------------------- #

import pandas as pd

def check_names(batterNamesAway, pitcherNameAway, batterNamesHome, pitcherNameHome):
	duplicateNames = ['Jose Ramirez', 'Chris Young', 'Daniel Robertson', 'Chris Smith']
	duplicateResolvers = ['Jose Ramirez, Indians', 'Jose Ramirez, Braves',
						  'Chris Young, Red Sox', 'Chris Young, Royals',
						  'Daniel Robertson, Rays', 'Daniel Robertson, Indians',
						  'Chris Smith, Athletics', 'Chris Smith, Blue Jays']

	invalidNames = []
	batterData = pd.read_csv('baseballsimulator/custom/2017FanGraphsBatting.csv')
	pitcherData = pd.read_csv('baseballsimulator/custom/2017FanGraphsPitching.csv')
	batterNameList = batterData['Name'].tolist()
	pitcherNameList = pitcherData['Name'].tolist()
	
	for battingOrder, batterNameAway in enumerate(batterNamesAway, start=1):
		if batterNameAway not in batterNameList or batterNameAway in duplicateNames:
			if batterNameAway not in duplicateResolvers:
				invalidNames.append("Away Batter " + str(battingOrder) + ": " +
									batterNameAway)
	
	if pitcherNameAway not in pitcherNameList or pitcherNameAway in duplicateNames:
		if pitcherNameAway not in duplicateResolvers:
			invalidNames.append("Away Pitcher: " + pitcherNameAway)
	
	for battingOrder, batterNameHome in enumerate(batterNamesHome, start=1):
		if batterNameHome not in batterNameList or batterNameHome in duplicateNames:
			if batterNameHome not in duplicateResolvers:
				invalidNames.append("Home Batter " + str(battingOrder) + ": " +
									batterNameHome)

	if pitcherNameHome not in pitcherNameList or pitcherNameHome in duplicateNames:
		if pitcherNameHome not in duplicateResolvers:
			invalidNames.append("Home Pitcher: " + pitcherNameHome)

	return invalidNames

# --------------------------------- Notes ----------------------------------- #
#
# Purpose: get_correct_player method makes sure to return the correct player
#		   object to views, after checking for players with same names or
#		   players with small sample sizes.
#
# For batters, there are 4 same-name players
#		- Jose Ramirez: Indians (playerid 13510), Braves (playerid 10171)
#		- Chris Young: Red Sox (playerid 3882), Royals (playerid 3196)
#		- Daniel Robertson: Rays (playerid 14145), Indians (playerid 6266)
#		- Chris Smith: Athletics (playerid 4544), Blue Jays (playerid 14449)
#
# For pitchers, there are 1 same-named player
#		- Chris Smith: Athletics (playerid 4544), Blue Jays (playerid 14449)
#
# --------------------------------------------------------------------------- #

# standalone script needs this to be able to use Django,
# and we need to use the Django database and models
import sys, os, django
from pathlib import Path
projectDir = Path(__file__).resolve().parents[2]
sys.path.append(str(projectDir))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baseballproject.settings.prod')
django.setup()

from baseballsimulator.models import Batter, Pitcher, League

def get_correct_player(playerName, position):
	playerObject = None
	duplicateResolvers = ['Jose Ramirez, Indians', 'Jose Ramirez, Braves',
						  'Chris Young, Red Sox', 'Chris Young, Royals',
						  'Daniel Robertson, Rays', 'Daniel Robertson, Indians',
						  'Chris Smith, Athletics', 'Chris Smith, Blue Jays']

	if position == 'batter':
		if playerName == 'Jose Ramirez, Indians':
			playerObject = Batter.objects.get(playerid=13510)
		elif playerName == 'Jose Ramirez, Braves':
			playerObject = Batter.objects.get(playerid=10171)
		elif playerName == 'Chris Young, Red Sox':
			playerObject = Batter.objects.get(playerid=3882)
		elif playerName == 'Chris Young, Royals':
			playerObject = Batter.objects.get(playerid=3196)
		elif playerName == 'Daniel Robertson, Rays':
			playerObject = Batter.objects.get(playerid=14145)
		elif playerName == 'Daniel Robertson, Indians':
			playerObject = Batter.objects.get(playerid=6266)
		elif playerName == 'Chris Smith, Athletics':
			playerObject = Batter.objects.get(playerid=4544)
		elif playerName == 'Chris Smith, Blue Jays':
			playerObject = Batter.objects.get(playerid=14449)
		else:
			playerObject = Batter.objects.get(name=playerName)

		if playerObject.pa < 15:
			return Batter.objects.get(name='Small Sample Batter')
		else:
			return playerObject

	else:  # position == 'pitcher'
		if playerName == 'Chris Smith, Athletics':
			playerObject = Pitcher.objects.get(playerid=4544)
		elif playerName == 'Chris Smith, Blue Jays':
			playerObject = Pitcher.objects.get(playerid=14449)
		else:
			playerObject = Pitcher.objects.get(name=playerName)

		if playerObject.tbf < 15:
			return Pitcher.objects.get(name='Small Sample Pitcher')
		else:
			return playerObject
