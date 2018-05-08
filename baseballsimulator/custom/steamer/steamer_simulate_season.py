# By: Junsoo Derek Shin
# Date: May 8, 2018

# ------------------------------- Description ------------------------------- #
# 
# Standalone program that simulates the 2017 MLB season using the 2017 Steamer
# projections and 2016 baserunning stats.
#
# The purpose of this program is to see how well the simulator simulates the
# baseball matches by comparing the average errors in teams' win-loss records
# with the FiveThirtyEight's and Steamer's season predictions, whose models 
# both use the Steamer projections. The simulator simulates 100 seasons and
# uses the average win-loss records for those seasons as its final win-loss
# predictions.
#
# Although this program is not part of the Django app, baseballsimulator, it is
# located here because it tests the simulation.py module, which is the core
# of the Django app.
#
# --------------------------------------------------------------------------- #


# --------------------------------- Notes ----------------------------------- #
#
# Steamer batting projections include lots of players including minor league
# players and exclude pitchers' batting projections. The same goes for the
# pitching projections -- tons of players and only pitchers.
#
# There were 7 batter names that showed up in the 2017 Retrosheet game logs 
# and were shared with other players. There were 6 such pitcher names.
#
# These numbers were different in FanGraphs because FanGraphs batting files
# had small number of players and included pitchers.
#
# http://www.retrosheet.org/gamelogs/glfields.txt
#		listed which information is recorded in the Retrosheet game logs.
#
# --------------------------------------------------------------------------- #

import sys
from pathlib import Path
projectDir = Path(__file__).resolve().parents[2]
sys.path.append(str(projectDir))
import custom.simulation as simulation
import pandas as pd

# create DataFrames and add extra columns to batter and pitcher DataFrames and 
# league Series.
# the columns are full names and probabilites for each event plate appearance.
def create_dataframes():
	batterDF = pd.read_csv('2017SteamerBatting.csv')
	pitcherDF = pd.read_csv('2017SteamerPitching.csv')
	leagueObject = None
	ssBatter = None
	ssPitcher = None

	batterDF = batterDF.assign(Name = batterDF['firstname'] + ' ' + batterDF['lastname'],
							   p1b = batterDF['1B'] / batterDF['PA'],
							   p2b = batterDF['2B'] / batterDF['PA'],
							   p3b = batterDF['3B'] / batterDF['PA'],
							   phr = batterDF['HR'] / batterDF['PA'],
							   ptw = (batterDF['BB'] + batterDF['HBP']) / batterDF['PA'],
							   pso = batterDF['K'] / batterDF['PA'],
							   pbo = (batterDF['PA'] - batterDF['H'] - batterDF['BB']
						          	  - batterDF['HBP'] - batterDF['K']) / batterDF['PA'])
	pitcherDF = pitcherDF.assign(Name = pitcherDF['firstname'] + ' ' + pitcherDF['lastname'],
								 p1b = pitcherDF['1b'] / pitcherDF['TBF'],
						   		 p2b = pitcherDF['2b'] / pitcherDF['TBF'],
						   		 p3b = pitcherDF['3b'] / pitcherDF['TBF'],
						   		 phr = pitcherDF['HR'] / pitcherDF['TBF'],
						   		 ptw = (pitcherDF['BB'] + pitcherDF['HBP']) / pitcherDF['TBF'],
						   		 pso = pitcherDF['K'] / pitcherDF['TBF'],
						   		 pbo = (pitcherDF['TBF'] - pitcherDF['H'] - pitcherDF['BB']
					          	        - pitcherDF['HBP'] - pitcherDF['K']) / pitcherDF['TBF'])
	batterDF.set_index('Name', inplace=True)
	pitcherDF.set_index('Name', inplace=True)

	leagueObject = batterDF.mean()
	ssBatter = batterDF.loc[batterDF['PA'] < 15].mean()
	ssPitcher = pitcherDF.loc[pitcherDF['TBF'] < 15].mean()
	return (batterDF, pitcherDF, leagueObject, ssBatter, ssPitcher)

# go through the game logs and simulate the season
def simulate_season(numGames, numSeasons, batterDF, pitcherDF, leagueObject, ssBatter, ssPitcher):
	numSuccessfulPredictions = 0
	with open('../2017gamelogs.txt', 'r') as infile, open('2017SteamerSimulations.txt', 'w') as outfile:
		outfile.write("index,awayTeam,winAway,runAway,homeTeam,winHome,runHome,"
					  + "predictedWinner,actualWinner,numSuccessfulPredictions\n")
		for index, line in enumerate(infile, start=1):
			gameInfo = [x.strip('\"') for x in line.split(',')]

			# store (retrosheet player id, player name) tuples
			batterInfoListAway = []
			batterInfoListHome = []
			for i in range(106, 133, 3):
				batterName = get_steamer_name(gameInfo[i])
				batterInfoListAway.append((gameInfo[i - 1], batterName))
			for i in range(133, 159, 3):
				batterName = get_steamer_name(gameInfo[i])
				batterInfoListHome.append((gameInfo[i - 1], batterName))

			pitcherInfoAway = (gameInfo[101], get_steamer_name(gameInfo[102]))
			pitcherInfoHome = (gameInfo[103], get_steamer_name(gameInfo[104]))

			# store batter, pitcher and league objects
			batterListAway = []
			batterListHome = []
			for batterInfoAway, batterInfoHome in zip(batterInfoListAway, batterInfoListHome):
				batterListAway.append(get_correct_batter_object(batterDF, ssBatter, 
																batterInfoAway))
				batterListHome.append(get_correct_batter_object(batterDF, ssBatter, 
																batterInfoHome))

			pitcherAway = get_correct_pitcher_object(pitcherDF, ssPitcher, pitcherInfoAway)
			pitcherHome = get_correct_pitcher_object(pitcherDF, ssPitcher, pitcherInfoHome)

			for i in range(numSeasons):
				winAway, winHome, runAway, runHome = simulation.simulate(numGames,
																		 batterListAway, pitcherAway, 
													   					 batterListHome, pitcherHome, 
													   					 leagueObject)
				predictedWinner = 'Home'
				if winAway > winHome:
					predictedWinner = 'Away'

				actualWinner = 'Home'
				# if the away team won in the actual game
				if int(gameInfo[9]) > int(gameInfo[10]):
					actualWinner = 'Away'

				if predictedWinner == actualWinner:
					numSuccessfulPredictions += 1

				outfile.write(str(index) + ',' 
							  + gameInfo[3] + ',' + str(winAway) + ',' + str(runAway) + ',' 
							  + gameInfo[6] + ',' + str(winHome) + ',' + str(runHome) + ',' 
							  + predictedWinner + ',' + actualWinner + ',' 
							  + str(numSuccessfulPredictions) + '\n')

# standalone function that:
#		- finds the differences in the Retrosheet and Steamer names
#		- finds the players who share names
def find_name_anomalies(batterDF, pitcherDF):
	steamerBatterNames = batterDF.index.tolist()
	steamerPitcherNames = pitcherDF.index.tolist()
	rsBatterNames = set()
	rsPitcherNames = set()
	with open('../2017gamelogs.txt', 'r') as f:
		for index, line in enumerate(f, start=1):
			gameInfo = [x.strip('\"') for x in line.split(',')]
			# add batters and pitchers names in the set
			for i in range(106, 159, 3):
				rsBatterNames.add((gameInfo[i], gameInfo[i-1]))
			rsPitcherNames.add((gameInfo[102], gameInfo[101]))
			rsPitcherNames.add((gameInfo[104], gameInfo[103]))

	pitcherDiff = rsPitcherNames - steamerPitcherNames
	batterDiff = rsBatterNames - rsPitcherNames - steamerBatterNames - steamerPitcherNames
	
	dupBatterNames = [(x, steamerBatterNames.count(x)) for x in rsBatterNames 
													   if steamerBatterNames.count(x) > 1]
	dupPitcherNames = [(x, steamerPitcherNames.count(x)) for x in rsPitcherNames 
														 if steamerPitcherNames.count(x) > 1]

# check for the unique Retrosheet name and return the Steamer name
def get_steamer_name(playerName):
	pitcherDiff = {
		'Nathan Karns': 'Nate Karns',
		'Michael Fiers': 'Mike Fiers',
		'Tom Milone': 'Tommy Milone',
		'Vincent Velasquez': 'Vince Velasquez',
		'Joe Biagini': 'Joseph Biagini',
		'J.C. Ramirez': 'JC Ramirez',
		'Deck McGuire': 'Deck Mcguire'
	}
	batterDiff = {
		'Dusty Coleman': 'Dustin Coleman',
		'J.T. Riddle': 'JT Riddle',
		'Alex Mejia': 'Alejandro Mejia',
		'Daniel Vogelbach': 'Dan Vogelbach',
		'Alejandro de Aza': 'Alejandro De Aza',
		'Steven Souza': 'Steven Souza Jr.',
		'Paul DeJong': 'Paul Dejong',
		'Mike Tauchman': 'Michael Tauchman',
		'Luke Voit': 'Louis Voit',
		'Rafael Lopez': 'Raffy Lopez',
		'Bruce Maxwell': 'Bruce Maxwell III',
		'Ryan McMahon': 'Ryan Mcmahon',
		'Yolmer Sanchez': 'Carlos Sanchez', 
		'Greg Bird': 'Gregory Bird',
		'Hyun Soo Kim': 'Hyun-soo Kim',
		'Chris Marrero': 'Christian Marrero',
		'Rickie Weeks': 'Rickie Weeks Jr.',
		'Cameron Perkins': 'Cam Perkins',
		'Jackie Bradley': 'Jackie Bradley Jr.'
	}
	if playerName in pitcherDiff:
		return pitcherDiff[playerName]
	elif playerName in batterDiff:
		return batterDiff[playerName]
	else:
		return playerName

# check for batters that:
#		- share the same names
#		- have small sample sizes
#		- do not exist in the Steamer DataFrame (in which case, we use the
#		  small sample batter object)
def get_correct_batter_object(batterDF, ssBatter, batterInfo):
	batterID = batterInfo[0]
	batterName = batterInfo[1]
	batterObject = None
	steamerBatterNames = batterDF.index.tolist()
	dupBatterTable = {
		'robed004': 'sa657854',  # Daniel Robertson, Rays
		'robed003': '6266',		 # Daniel Robertson, Indians
		'martj008': '7996',		 # Jose Martinez, Cardinals
		'vazqc001': '9774',		 # Chrisian Vazquez, Red Sox
		'perec003': '10642',	 # Carlos Perez, Angels
		'gonzc001': '7287',		 # Carlos Gonzalez, Rockies
		'moort002': '7244',		 # Tyler Moore, Marlins
		'sancc001': '11602'		 # Yolmer Sanchez (Carlos Sanchez), White Sox
	}

	if batterID in dupBatterTable:
		steamerID = dupBatterTable[batterID]
		batterObject = batterDF.loc[batterDF['steamerid'] == steamerID].squeeze()
	elif batterName not in steamerBatterNames:
		batterObject = ssBatter
	else:
		batterObject = batterDF.loc[batterName]

	if batterObject['PA'] < 15:
		return ssBatter
	else:
		return batterObject

def get_correct_pitcher_object(pitcherDF, ssPitcher, pitcherInfo):
	pitcherID = pitcherInfo[0]
	pitcherName = pitcherInfo[1]
	pitcherObject = None
	steamerPitcherNames = pitcherDF.index.tolist()
	dupPitcherTable = {
		'castl003': 'sa657487',  # Luis Castillo, Reds
		'gonzm003': '7024',		 # Miguel Gonzales, White Sox
		'smitc002': '4544',		 # Chris Smith, Athletics
		'thomj007': '14371',	 # Jake Thompson, Phillies
		'reedc002': '15232',	 # Cody Reed, Reds
		'smitc006': 'sa738884'	 # Caleb Smith, Yankees
	}

	if pitcherID in dupPitcherTable:
		steamerID = dupPitcherTable[pitcherID]
		pitcherObject = pitcherDF.loc[pitcherDF['steamerid'] == steamerID].squeeze()
	elif pitcherName not in steamerPitcherNames:
		pitcherObject = ssPitcher
	else:
		pitcherObject = pitcherDF.loc[pitcherName]

	if  pitcherObject['TBF'] < 15:
		return ssPitcher
	else:
		return pitcherObject

# calculate mean absolute errors for the FiveThirtyEight and Steamer preseason
# predictions
def calc_third_party_simulations_errors():
	MLBResults = [93,76,80,91,75,102,64,85,80,67,101,78,78,80,75,97,70,77,72,66,92,83,75,86,68,104,64,93,87,71]
	FTEPreds = [88,84,81,80,78,94,82,74,74,73,90,86,81,79,75,92,87,80,74,70,98,81,81,74,72,95,88,76,75,68]
	SteamerPreds = [91,86,81,79,80,94,82,75,76,68,90,82,82,83,77,92,87,79,72,72,97,85,80,70,68,97,88,77,78,66]
	FTEErrors = [abs(x - y) for x, y in zip(FTEPreds, MLBResults)]
	SteamerErrors = [abs(x - y) for x, y in zip(SteamerPreds, MLBResults)]
	FTEMeanErrors = sum(FTEErrors) / len(FTEErrors)
	SteamerMeanErrors = sum(SteamerErrors) / len(SteamerErrors)

# calculate mean absolute error for the predictions that came from the
# simulations
def calc_my_simulations_errors(numSeasons):
	MLBResults = [93,76,80,91,75,102,64,85,80,67,101,78,78,80,75,97,70,77,72,66,92,83,75,86,68,104,64,93,87,71]
	teams = ['BOS','TOR','TBA','NYA','BAL',
			 'CLE','DET','MIN','KCA','CHA',
			 'HOU','SEA','TEX','ANA','OAK',
			 'WAS','NYN','MIA','ATL','PHI',
			 'CHN','SLN','PIT','MIL','CIN',
			 'LAN','SFN','ARI','COL','SDN']
	predSeries = pd.Series(data=[0]*30, index=teams)
	simulationsDF = pd.read_csv('2017SteamerSimulations.txt')
	for index, row in simulationsDF.iterrows():
		prediction = row['predictedWinner']
		if prediction == 'Home':
			winner = row['homeTeam']
		else:
			winner = row['awayTeam']
		predSeries.loc[winner] += 1

	myPreds = predSeries.values.tolist()
	myPreds = [round(x / numSeasons) for x in myPreds]
	myErrors = [abs(x - y) for x, y in zip(myPreds, MLBResults)]
	myMeanErrors = sum(myErrors) / len(myErrors)
	print(myMeanErrors)

def main():
	numGames = 1
	numSeasons = 100
	batterDF, pitcherDF, leagueObject, ssBatter, ssPitcher = create_dataframes()
	simulate_season(numGames, numSeasons, batterDF, pitcherDF, leagueObject, ssBatter, ssPitcher)
	calc_my_simulations_errors(numSeasons)
	
if __name__ == "__main__":
	main()
