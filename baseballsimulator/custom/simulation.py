# Given the lists of batter, pitcher and league objects, run simulations using
# their records and return the away and home winning percentages.
#
# results() view calls this program to get the simulation results.

import pandas as pd
from numpy.random import choice
from pathlib import Path

# calculates and returns the list of probabilities of each outcome of a plate 
# appearance
def calcOddsRatio(batter, pitcher, league):
  # Tom Tango's Odds Ratio Method
  odds1b = ((batter.p1b / (1-batter.p1b)) * (pitcher.p1b / (1-pitcher.p1b)) 
           / (league.p1b / (1-league.p1b)))
  odds2b = ((batter.p2b / (1-batter.p2b)) * (pitcher.p2b / (1-pitcher.p2b)) 
           / (league.p2b / (1-league.p2b)))
  odds3b = ((batter.p3b / (1-batter.p3b)) * (pitcher.p3b / (1-pitcher.p3b)) 
           / (league.p3b / (1-league.p3b)))
  oddshr = ((batter.phr / (1-batter.phr)) * (pitcher.phr / (1-pitcher.phr))
           / (league.phr / (1-league.phr)))
  oddstw = ((batter.ptw / (1-batter.ptw)) * (pitcher.ptw / (1-pitcher.ptw)) 
           / (league.ptw / (1-league.ptw)))
  oddsso = ((batter.pso / (1-batter.pso)) * (pitcher.pso / (1-pitcher.pso)) 
           / (league.pso / (1-league.pso)))
  oddsbo = ((batter.pbo / (1-batter.pbo)) * (pitcher.pbo / (1-pitcher.pbo)) 
           / (league.pbo / (1-league.pbo)))
  # turn odds into probabilities
  p1b = odds1b / (odds1b + 1)
  p2b = odds2b / (odds2b + 1)
  p3b = odds3b / (odds3b + 1)
  phr = oddshr / (oddshr + 1)
  ptw = oddstw / (oddstw + 1)
  pso = oddsso / (oddsso + 1)
  pbo = oddsbo / (oddsbo + 1)
  total = p1b + p2b + p3b + phr + ptw + pso + pbo
  # probabilities from the Odds Ratio Method don't exactly add up to 1 used
  # in this way, so they are normalized here
  np1b = p1b / total
  np2b = p2b / total
  np3b = p3b / total
  nphr = phr / total
  nptw = ptw / total
  npso = pso / total
  npbo = pbo / total
  return [np1b, np2b, np3b, nphr, nptw, npso, npbo] 

# plays an entire game and returns 0 if the away team wins and 1 if the home
# team wins or draws
def playGame(batterListAway, pitcherAway, batterListHome, pitcherHome, league, brDF):
  inning = 0
  out = 0
  bases = "000"
  state = "0,000"
  battingOrderHome = 0
  battingOrderAway = 0
  scoreHome = 0
  scoreAway = 0
  playList = ["1b", "2b", "3b", "hr", "tw", "so", "bo"]

  # play from top 1st to bottom 9th inning, and extra innings are upto 33rd
  #   - i goes from 10 to 3300, and inning goes from 1 to 33
  #   - inning indicates the start of the inning (if inning is 9.5, that means
  #     the start of the bottom 9th)
  for inning in [i / 10 for i in range(10,3305,5)]:
    if inning == 9.5 and scoreAway < scoreHome:  # home team won; don't play bottom 9th
      break
    elif inning >= 10.0 and (inning % 1.0) == 0.0:  # end of 9th and extra innings (one inning sudden death)
      if scoreAway != scoreHome:
        break

    if (inning % 1.0) == 0.0:  # away team bats
      batter = batterListAway[battingOrderAway]
      pitcher = pitcherHome
      score = scoreAway
      battingOrder = battingOrderAway
    else:  # home team bats
      batter = batterListHome[battingOrderHome]
      pitcher = pitcherAway
      score = scoreHome
      battingOrder = battingOrderHome
    while out < 3:
      playProbList = calcOddsRatio(batter, pitcher, league)
      play = choice(playList, p=playProbList)
      if play == "1b" or play == "2b" or play == "3b" or play == "bo":
        brDict = brDF.loc[state, play]
        # keys() and values() methods are not supposed to preserve the order, but they seem to do so
        resultList = list(brDict.keys())[1:]  # list of possible resulting states
        countList = list(brDict.values())[1:]  # list of number of occurrences of those resulting states
        totalCount = brDict['total']  # number of occurrences of this starting state and the play combination
        probList = [count / totalCount for count in countList]
        result = choice(resultList, p=probList)
        out = int(result.split(",")[0])
        bases = result.split(",")[1]
        score += int(result.split(",")[2])
      elif play == "hr":
        score += (int(bases[0]) + int(bases[1]) + int(bases[2]) + 1)
        bases = "000"
      elif play == "tw":
        if bases == "000" or bases == "001" or bases == "010":
          bases = str(int(bases) | 100)
        elif bases == "100":
          bases = "110"
        elif bases == "110" or bases == "011" or bases == "101":
          bases = "111"
        else:
          bases = "111"
          score += 1
      else:  #play == "so"
        out += 1

      state = str(out) + "," + bases
      if battingOrder < 8:
        battingOrder += 1
      else:
        battingOrder = 0

    # update the score and batting order for the correct team
    if (inning % 1.0) == 0.0:
      scoreAway = score
      battingOrderAway = battingOrder
    else:
      scoreHome = score
      battingOrderHome = battingOrder
    # reset for the next inning
    out =  0
    bases = "000"
    state = "0,000"

  if scoreAway > scoreHome:
    return (0, scoreAway, scoreHome)
  else:
    return (1, scoreAway, scoreHome)

# simulates games between two teams and returns the winning percentages
def simulate(numGames, batterListAway, pitcherAway, batterListHome, pitcherHome, league):
  parentDir = Path(__file__).resolve().parent
  baserunningFilePath = parentDir.joinpath('2017baserunning.pkl')
  brDF = pd.read_pickle(baserunningFilePath)
  winAway = 0
  winHome = 0
  runAway = 0
  runHome = 0
  for i in range(0, numGames):
    result = playGame(batterListAway, pitcherAway, batterListHome, pitcherHome, league, brDF)
    runAway += result[1]
    runHome += result[2]
    if result[0] == 0:
      winAway += 1
    else:
      winHome += 1
  winningPercentageAway = int((winAway / numGames) * 100)
  winningPercentageHome = 100 - winningPercentageAway
  return (winningPercentageAway, winningPercentageHome, runAway, runHome)