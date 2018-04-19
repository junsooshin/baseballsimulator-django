# Create batters, pitchers, and league models.
#
# I ran this program beforehand to save the models in the database.

import os, sys, django
sys.path.append('/Users/JunSooShin/Desktop/baseballsimulator-django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baseballproject.settings.prod')
django.setup()

import csv
from baseballsimulator.models import Batter, Pitcher, League

with open('./2017FanGraphsBatting.csv') as f:
	headerLine = f.readline()
	reader = csv.reader(f)
	for row in reader:
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

with open('./2017FanGraphsPitching.csv') as f:
	headerLine = f.readline()
	reader = csv.reader(f)
	for row in reader:
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

with open('./2017FanGraphsLeague.csv') as f:
	headerLine = f.readline()
	reader = csv.reader(f)
	for row in reader:
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