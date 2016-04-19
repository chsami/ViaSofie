from django.db import models

class Gebruiker(models.Model):
    #Id implemented by django
    #userid = models.Autofield(primary_key=True)
    voornaam = models.charField(max_length=128)
    naam =  models.charField(max_length=128)
    email = models.charField(max_length=128)
    straatnaam = models.charField(max_length=128)
    huisnr = models.IntegerField()
    postcode = models.IntegerField()
    busnr = models.charField(max_length=10)
    telefoonnr = models.IntegerField()
    password= models.charField(max_length=30) #ToDo: add hashes + saltes (import)
    toegangslevel = models.ForeignKey(Toegangslevel)

    def __str__(self):
        return self.id
#authentication https://docs.djangoproject.com/en/1.9/topics/auth/customizing/

class Log(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    gebruiker = models.ForeignKey(Gebruiker)
    logText = models.charField(255)
    
    def __str__(self):
        return self.id

class Toegangslevel(models.Model):
    toegangslevelnaam = models.charField(255)
    
    def __str__(self):
        return self.id

class Pand(models.Model):
	#id autocreated by django
    gebruiker = models.ForeignKey(Gebruiker)
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