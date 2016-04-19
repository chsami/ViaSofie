from django.db import models

# Create your models here.
class Pand(models.Model):
	#id autocreated by django
	straatnaam = models.CharField(max_length=128)
	huisnr = models.SmallIntegerField
	postcodeID = models.ForeignKey(Steden)
	pandtype = models.ForeignKey(Pandtype)
	handelstatus = models.ForeignKey(Handelstatus)
	voortgang = models.ForeignKey(Voortgang)

	def __str__(self):
        return self.id


class Tag(models.Model):
    #id autocreated by django
    tagnaam = models.CharField(max_length=128)
    Pand = models.ManyToManyField(Panden)

	def __str__(self):
        return self.id


class Stad(models.Model):
	postcode = models.SmallIntegerField
	stadsnaam = models.CharField(max_length=128)

	def __str__(self):
        return self.id

class Foto(models.Model):
	url = models.CharField(max_length=256)
	pand = models.ManyToManyField(Panden)

	def __str__(self):
        return self.id


class PandType(model.Model):
	pandtype = models.CharField(max_length=128) #kantoor,huis, appartement, ...

	def __str__(self):
        return self.id


class Handelstatus(models.Model)
	status = models.CharField(max_length=128) #verkoop, verhuur, verpachten, ...

	def __str__(self):
        return self.id


class Voortgang(models.Model)
	status = models.Charfiels(max_length=128) #online, optie, bij notaris, ...

	def __str__(self):
        return self.id


