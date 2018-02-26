from django.db import models

# Create your models here.
class Batter(models.Model):
	name = models.CharField(max_length=50)
	team = models.CharField(max_length=50)
	game = models.IntegerField()
	ab = models.IntegerField()
	pa = models.IntegerField()
	hit = models.IntegerField()
	single = models.IntegerField()
	double = models.IntegerField()
	triple = models.IntegerField()
	hr = models.IntegerField()
	run = models.IntegerField()
	rbi = models.IntegerField()
	bb = models.IntegerField()
	ibb = models.IntegerField()
	so = models.IntegerField()
	hbp = models.IntegerField()
	
	playerid = models.IntegerField()
	year = models.IntegerField()

	p1b = models.FloatField()
	p2b = models.FloatField()
	p3b = models.FloatField()
	phr = models.FloatField()
	ptw = models.FloatField()
	pso = models.FloatField()
	pbo = models.FloatField()

	def __str__(self):
		return self.name

class Pitcher(models.Model):
	name = models.CharField(max_length=50)
	playerid = models.IntegerField()
	year = models.IntegerField()
	team = models.CharField(max_length=50)
	
	ip = models.FloatField()
	tbf = models.IntegerField()
	hit = models.IntegerField()
	single = models.IntegerField()
	double = models.IntegerField()
	triple = models.IntegerField()
	run = models.IntegerField()
	er = models.IntegerField()
	hr = models.IntegerField()
	bb = models.IntegerField()
	ibb = models.IntegerField()
	hbp = models.IntegerField()
	so = models.IntegerField()

	p1b = models.FloatField()
	p2b = models.FloatField()
	p3b = models.FloatField()
	phr = models.FloatField()
	ptw = models.FloatField()
	pso = models.FloatField()
	pbo = models.FloatField()

	def __str__(self):
		return self.name

class League(models.Model):
	season = models.IntegerField()
	game = models.IntegerField()
	ab = models.IntegerField()
	pa = models.IntegerField()
	hit = models.IntegerField()
	single = models.IntegerField()
	double = models.IntegerField()
	triple = models.IntegerField()
	hr = models.IntegerField()
	run = models.IntegerField()
	rbi = models.IntegerField()
	bb = models.IntegerField()
	ibb = models.IntegerField()
	so = models.IntegerField()
	hbp = models.IntegerField()

	year = models.IntegerField()

	p1b = models.FloatField()
	p2b = models.FloatField()
	p3b = models.FloatField()
	phr = models.FloatField()
	ptw = models.FloatField()
	pso = models.FloatField()
	pbo = models.FloatField()

	def __str__(self):
		return str(self.season)