# Check the batter and pitcher names using the FanGraphs csv files and return
# invalid player names in a string list.
#
# results() view uses this program to see if there are invalid player names
# before using objects.get().

import pandas as pd

def check_names(batterNamesAway, pitcherNameAway, batterNamesHome, pitcherNameHome):
	invalidNames = []
	batterData = pd.read_csv('baseballsimulator/custom/2017FanGraphsBatting.csv')
	pitcherData = pd.read_csv('baseballsimulator/custom/2017FanGraphsPitching.csv')
	batterNameList = batterData['Name'].tolist()
	pitcherNameList = pitcherData['Name'].tolist()
	
	for battingOrder, batterNameAway in enumerate(batterNamesAway, start=1):
		if batterNameAway not in batterNameList:
			invalidNames.append("Away Batter " + str(battingOrder) + ": " +
								batterNameAway)
	
	if pitcherNameAway not in pitcherNameList:
		invalidNames.append("Away Pitcher: " + pitcherNameAway)
	
	for battingOrder, batterNameHome in enumerate(batterNamesHome, start=1):
		if batterNameHome not in batterNameList:
			invalidNames.append("Home Batter " + str(battingOrder) + ": " +
								batterNameHome)

	if pitcherNameHome not in pitcherNameList:
		invalidNames.append("Home Pitcher: " + pitcherNameHome)

	return invalidNames