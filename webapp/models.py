from django.db import models

# Create your models here.
class Panden(models.Model):
	#id autocreated by django
	straatnaam = models.CharField(max_length=128)
	huisnr = models.SmallIntegerField
	postcodeID = models.ForeignKey(Steden)
	pandtype = models.ForeignKey(Pandtype)
	handelstatus = models.ForeignKey(Handelstatus)
	voortgang = models.ForeignKey(Voortgang)


class Tags(models.Model):
    #id autocreated by django
    tagnaam = models.CharField(max_length=128)
    Pand = models.ManyToManyField(Panden)


class Steden(models.Model):
	postcode = models.SmallIntegerField
	stadsnaam = models.CharField(max_length=128)

class Fotos(models.Model):
	url = models.CharField(max_length=256)
	pand = models.ManyToManyField(Panden)

class PandType(model.Model):
	pandtype = models.CharField(max_length=128) #kantoor,huis, appartement, ...

class Handelstatus(models.Model)
	status = models.CharField(max_length=128) #verkoop, verhuur, verpachten, ...

class Voortgang(models.Model)
	status = models.Charfiels(max_length=128) #online, optie, bij notaris, ...

