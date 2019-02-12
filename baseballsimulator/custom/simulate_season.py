# By: Junsoo Derek Shin
# Date: April 14, 2018

# ------------------------------- Description ------------------------------- #
#
# Run 1000 simulations for each of the 2034 games from the 2017 MLB season,
#     using the same starting lineups.
#
# For each game, the winner is the team with more simulated wins.
#     (if there is a tie -- 500 wins and 500 losses -- then the tie will go to 
#      the home team.)
#
# Out of the 2430 games, count the number of game the simulator correctly 
#     guesses the results.
#
# --------------------------------------------------------------------------- #


# --------------------------------- Notes ----------------------------------- #
#
# For batters, there are 4 same-name players
#   - Jose Ramirez: ramij003 Indians (playerid 13510), ramij004 Braves (playerid 10171)
#   - Chris Young: younc004 Red Sox (playerid 3882), younc003 Royals (playerid 3196)
#   - Daniel Robertson: robed004 Rays (playerid 14145), robed003 Indians (playerid 6266)
#   - Chris Smith: smithc002 Athletics (playerid 4544)
#
# For pitchers, there are 1 same-named player
#   - Chris Smith: smithc002 Athletics (playerid 4544)
#
#   * Blue Jays' Chris Smith (playerid 14449) was a reliever, so he doesn't
#         show up in the 2017 game logs. We still have to make sure to choose
#     the Athletics' Chris Smith.
#
# http://www.retrosheet.org/gamelogs/glfields.txt
#   listed which information is recorded in the Retrosheet game logs.
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
import simulation
import pandas as pd

def simulate_season(numGames):
  numSuccessfulPredictions = 0
  with open('2017gamelogs.txt', 'r') as infile, open('2017simulations.txt', 'w') as outfile:
    outfile.write("index,awayTeam,winAway,runAway,homeTeam,winHome,runHome,"
            + "predictedWinner,actualWinner,numSuccessfulPredictions\n")
    for index, line in enumerate(infile, start=1):
      gameInfo = [x.strip('\"') for x in line.split(',')]

      # store (retrosheet player id, player name) tuples
      batterInfoListAway = []
      batterInfoListHome = []
      for i in range(106, 133, 3):
        batterName = get_fangraphs_name(gameInfo[i])
        batterInfoListAway.append((gameInfo[i - 1], batterName))
      for i in range(133, 159, 3):
        batterName = get_fangraphs_name(gameInfo[i])
        batterInfoListHome.append((gameInfo[i - 1], batterName))

      pitcherInfoAway = (gameInfo[101], get_fangraphs_name(gameInfo[102]))
      pitcherInfoHome = (gameInfo[103], get_fangraphs_name(gameInfo[104]))

      # store batter, pitcher and league objects
      batterListAway = []
      batterListHome = []
      for batterInfoAway, batterInfoHome in zip(batterInfoListAway, batterInfoListHome):
        batterListAway.append(get_correct_batter_object(batterInfoAway))
        batterListHome.append(get_correct_batter_object(batterInfoHome))

      pitcherAway = get_correct_pitcher_object(pitcherInfoAway)
      pitcherHome = get_correct_pitcher_object(pitcherInfoHome)
      league = League.objects.get(year=2017)
      winAway, winHome, runAway, runHome = simulation.simulate(numGames,
                                   batterListAway, pitcherAway, 
                                     batterListHome, pitcherHome, 
                                     league)
      predictedWinner = 'Home'
      if winAway > winHome:
        predictedWinner = 'Away'

      actualWinner = 'Home'
      # if the away team won in the actual game
      if int(gameInfo[9]) > int(gameInfo[10]):
        actualWinner = 'Away'

      if predictedWinner == actualWinner:
        numSuccessfulPredictions += 1

      print(index)
      # index, winAway, winHome, predictedWinner, actualWinner, numSuccessfulPredictions
      outfile.write(str(index) + ',' 
              + gameInfo[3] + ',' + str(winAway) + ',' + str(runAway) + ',' 
              + gameInfo[6] + ',' + str(winHome) + ',' + str(runHome) + ',' 
              + predictedWinner + ',' + actualWinner + ',' 
              + str(numSuccessfulPredictions) + '\n')

# check for the unique Retrosheet name and return the FanGraphs name
def get_fangraphs_name(playerName):
  diffNames = {'Greg Bird': 'Gregory Bird', 
         'Steven Souza': 'Steven Souza Jr.',
               'Jackie Bradley': 'Jackie Bradley Jr.',
               'Albert Almora': 'Albert Almora Jr.',
               'Rickie Weeks': 'Rickie Weeks Jr.',
               'Vincent Velasquez': 'Vince Velasquez',
               'Michael Fiers': 'Mike Fiers',
               'Tom Milone': 'Tommy Milone',
               'Nick Castellanos': 'Nicholas Castellanos',
               'J.C. Ramirez': 'JC Ramirez',
               'Michael Taylor': 'Michael A. Taylor',
               'Daniel Vogelbach': 'Dan Vogelbach',
               'Reymond Fuentes': 'Rey Fuentes',
               'Lance McCullers': 'Lance McCullers Jr.', # name in pitcher and batter files were different, so I just fixed it on Excel
               'Jake Junis': 'Jakob Junis',
               'Jacob Faria': 'Jake Faria',
               'Cameron Perkins': 'Cam Perkins',
               'Lucas Sims': 'Luke Sims',
               'Nicky Delmonico': 'Nick Delmonico',
               'Rafael Lopez': 'Raffy Lopez',
               'Alejandro de Aza': 'Alejandro De Aza',
  }

  if playerName in diffNames:
    return diffNames[playerName]
  else:
    return playerName

# check for batters that share the same name or have small sample size and 
# return the correct batter object
def get_correct_batter_object(batterInfo):
  batterID = batterInfo[0]
  batterName = batterInfo[1]
  batterObject = None

  if batterID == 'ramij003':  # Jose Ramirez, Indians
    batterObject = Batter.objects.get(playerid=13510)
  elif batterID == 'ramij004':  # Jose Ramirez, Braves
    batterObject = Batter.objects.get(playerid=10171)
  elif batterID == 'younc004':  # Chris Young, Red Sox
    batterObject = Batter.objects.get(playerid=3882)
  elif batterID == 'younc003':  # Chris Young, Royals
    batterObject = Batter.objects.get(playerid=3196)
  elif batterID == 'robed004':  # Daniel Robertson, Rays
    batterObject = Batter.objects.get(playerid=14145)
  elif batterID == 'robed003':  # Daniel Robertson, Indians
    batterObject = Batter.objects.get(playerid=6266)
  else:
    batterObject = Batter.objects.get(name=batterName)

  if batterObject.pa < 15:
    return Batter.objects.get(name='Small Sample Batter')
  else:
    return batterObject

def get_correct_pitcher_object(pitcherInfo):
  pitcherID = pitcherInfo[0]
  pitcherName = pitcherInfo[1]
  pitcherObject = None

  if pitcherID == 'smitc002':  # Chris Smith, Athletics
    pitcherObject = Pitcher.objects.get(playerid=4544)
  else:
    pitcherObject = Pitcher.objects.get(name=pitcherName)

  if pitcherObject.tbf < 15:
    return Pitcher.objects.get(name='Small Sample Pitcher')
  else:
    return pitcherObject

# check for names not in FanGraphs and print them.
# used for debugging.
def print_invalid_names(batterInfoListAway, pitcherInfoAway, batterInfoListHome, pitcherInfoHome):
  batterNamesAway = [x[1] for x in batterInfoListAway]
  batterNamesHome = [x[1] for x in batterInfoListHome]
  pitcherNameAway = pitcherInfoAway[1]
  pitcherNameHome = pitcherInfoHome[1]

  invalidNames = []
  batterDF = pd.read_csv('2017FanGraphsBatting.csv')
  pitcherDF = pd.read_csv('2017FanGraphsPitching.csv')
  batterNameList = batterDF['Name'].tolist()
  pitcherNameList = pitcherDF['Name'].tolist()

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

  if invalidNames:
    print(invalidNames)

def main():
  numGames = 1000
  simulate_season(numGames)
  
if __name__ == "__main__":
  main()