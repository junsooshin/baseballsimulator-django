# Create batters, pitchers, and league models.
#
# I ran this program beforehand to save the models in the database.

import os, sys, django
from pathlib import Path
projectDir = Path(__file__).resolve().parents[2]
sys.path.append(str(projectDir))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baseballproject.settings.prod')
django.setup()

import csv
from baseballsimulator.models import Batter, Pitcher, League

def fill_batter_objects():
	with open('2017FanGraphsBatting.csv') as f:
		headerLine = f.readline()
		for line in f:
			row = line.split(',')
			_, created = Batter.objects.get_or_create(
				name = row[0],
				team = row[1],
				game = int(row[2]),
				ab = int(row[3]),
				pa = int(row[4]),
				hit = int(row[5]),
				single = int(row[6]),
				double = int(row[7]),
				triple = int(row[8]),
				hr = int(row[9]),
				run = int(row[10]),
				rbi = int(row[11]),
				bb = int(row[12]),
				ibb = int(row[13]),
				so = int(row[14]),
				hbp = int(row[15]),
				playerid = int(row[22]),
				year = 2017,

				p1b = int(row[6]) / int(row[4]) if int(row[4]) != 0 else 0,
				p2b = int(row[7]) / int(row[4]) if int(row[4]) != 0 else 0,
				p3b = int(row[8]) / int(row[4]) if int(row[4]) != 0 else 0,
				phr = int(row[9]) / int(row[4]) if int(row[4]) != 0 else 0,
				ptw = (int(row[12]) + int(row[13]) + int(row[15])) / int(row[4]) if int(row[4]) != 0 else 0,
				pso = int(row[14]) / int(row[4]) if int(row[4]) != 0 else 0,
				pbo = (int(row[4]) - int(row[6]) - int(row[7]) - int(row[8]) 
					   - int(row[9]) - int(row[12]) - int(row[13]) - int(row[14])
					   - int(row[15])) / int(row[4]) if int(row[4]) != 0 else 0,
			)

def fill_pitcher_ojbects():
	with open('2017FanGraphsPitching.csv') as f:
		headerLine = f.readline()
		for line in f:
			row = line.split(',')
			_, created = Pitcher.objects.get_or_create(
				name = row[1],
				playerid = int(row[2]),
				year = int(row[0]),
				team = row[3],
				ip = float(row[4]),
				tbf = int(row[5]),
				hit = int(row[6]),
				single = int(row[6]) - int(row[7]) - int(row[8]) - int(row[11]),
				double = int(row[7]),
				triple = int(row[8]),
				run = int(row[9]),
				er = int(row[10]),
				hr = int(row[11]),
				bb = int(row[12]),
				ibb = int(row[13]),
				hbp = int(row[14]),
				so = int(row[15]),

				p1b = (int(row[6]) - int(row[7]) - int(row[8]) - int(row[11])) 
					   / int(row[5]) if int(row[5]) != 0 else 0,
				p2b = int(row[7]) / int(row[5]) if int(row[5]) != 0 else 0,
				p3b = int(row[8]) / int(row[5]) if int(row[5]) != 0 else 0,
				phr = int(row[11]) / int(row[5]) if int(row[5]) != 0 else 0,
				ptw = (int(row[12]) + int(row[13]) + int(row[14])) / int(row[5]) if int(row[5]) != 0 else 0,
				pso = int(row[15]) / int(row[5]) if int(row[5]) != 0 else 0,
				pbo = (int(row[5]) - int(row[6]) - int(row[12]) - int(row[13]) 
					   - int(row[14]) - int(row[15])) / int(row[5]) if int(row[5]) != 0 else 0,
			)

def fill_league_objects():
	with open('2017FanGraphsLeague.csv') as f:
		headerLine = f.readline()
		for line in f:
			row = line.split(',')
			_, created = League.objects.get_or_create(
				season = int(row[0]),
				game = int(row[1]),
				ab = int(row[2]),
				pa = int(row[3]),
				hit = int(row[4]),
				single = int(row[5]),
				double = int(row[6]),
				triple = int(row[7]),
				hr = int(row[8]),
				run = int(row[9]),
				rbi = int(row[10]),
				bb = int(row[11]),
				ibb = int(row[12]),
				so = int(row[13]),
				hbp = int(row[14]),
				year = 2017,

				p1b = int(row[5]) / int(row[3]) if int(row[3]) != 0 else 0,
				p2b = int(row[6]) / int(row[3]) if int(row[3]) != 0 else 0,
				p3b = int(row[7]) / int(row[3]) if int(row[3]) != 0 else 0,
				phr = int(row[8]) / int(row[3]) if int(row[3]) != 0 else 0,
				ptw = (int(row[11]) + int(row[12]) + int(row[14])) / int(row[3]) if int(row[3]) != 0 else 0,
				pso = int(row[13]) / int(row[3]) if int(row[3]) != 0 else 0,
				pbo = (int(row[3]) - int(row[5]) - int(row[6]) - int(row[7]) 
					   - int(row[8]) - int(row[11]) - int(row[12]) - int(row[13])
					   - int(row[14])) / int(row[3]) if int(row[3]) != 0 else 0,
			)

# create a dummy batter whose stats are average of all batters with small 
# samples and do the same for the pitchers
def fill_small_sample_players():
	batterDF = pd.read_csv('2017FanGraphsBatting.csv')
	pitcherDF = pd.read_csv('2017FanGraphsPitching.csv')
	ssBatterDF = batterDF[batterDF['PA'] < 15]
	ssPitcherDF = pitcherDF[pitcherDF['TBF'] < 15]
	avgPA = ssBatterDF['PA'].mean()
	avgTBF = ssPitcherDF['TBF'].mean()
	
	_, created = Batter.objects.get_or_create(
		name = 'Small Sample Batter',
		year = 2017,
		team = 'None',
		playerid = -1,

		game = -1,
		ab = -1,
		pa = -1,
		hit = -1,
		single = -1,
		double = -1,
		triple = -1,
		hr = -1,
		run = -1,
		rbi = -1,
		bb = -1,
		ibb = -1,
		so = -1,
		hbp = -1,

		p1b = ssBatterDF['1B'].mean() / avgPA,
		p2b = ssBatterDF['2B'].mean() / avgPA,
		p3b = ssBatterDF['3B'].mean() / avgPA,
		phr = ssBatterDF['HR'].mean() / avgPA,
		ptw = (ssBatterDF['BB'].mean() + ssBatterDF['IBB'].mean() + ssBatterDF['HBP'].mean()) / avgPA,
		pso = ssBatterDF['SO'].mean() / avgPA,
		pbo = (avgPA - ssBatterDF['1B'].mean() - ssBatterDF['2B'].mean() 
			   - ssBatterDF['3B'].mean() - ssBatterDF['HR'].mean() 
			   - ssBatterDF['BB'].mean() - ssBatterDF['IBB'].mean() 
			   - ssBatterDF['HBP'].mean() - ssBatterDF['SO'].mean()) / avgPA
	)

	_, created = Pitcher.objects.get_or_create(
		name = 'Small Sample Pitcher',
		year = 2017,
		team = 'None',
		playerid = -2,

		ip = -2,
		tbf = -2,
		hit = -2,
		single = -2,
		double = 2,
		triple = -2,
		hr = -2,
		run = -2,
		er = -2,
		bb = -2,
		ibb = -2,
		so = -2,
		hbp = -2,

		p1b = (ssPitcherDF['H'].mean() - ssPitcherDF['2B'].mean() 
			   - ssPitcherDF['3B'].mean() - ssPitcherDF['HR'].mean()) / avgTBF,
		p2b = ssPitcherDF['2B'].mean() / avgTBF,
		p3b = ssPitcherDF['3B'].mean() / avgTBF,
		phr = ssPitcherDF['HR'].mean() / avgTBF,
		ptw = (ssPitcherDF['BB'].mean() + ssPitcherDF['IBB'].mean() 
			   + ssPitcherDF['HBP'].mean()) / avgTBF,
		pso = ssPitcherDF['SO'].mean() / avgTBF,
		pbo = (avgTBF - ssPitcherDF['H'].mean() - ssPitcherDF['BB'].mean() 
			   - ssPitcherDF['IBB'].mean() - ssPitcherDF['HBP'].mean() 
			   - ssPitcherDF['SO'].mean()) / avgTBF
	)

def main():
	fill_batter_objects()
	fill_pitcher_ojbects()
	fill_league_objects()
	fill_small_sample_players()

if __name__ == "__main__":
	main()
