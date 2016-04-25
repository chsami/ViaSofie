from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser



class PandType(models.Model):
    pandtype = models.CharField(max_length=128) #kantoor,huis, appartement, ...

    def __str__(self):
        return self.id


class Handelstatus(models.Model):
    status = models.CharField(max_length=128) #verkoop, verhuur, verpachten, ...

    def __str__(self):
        return self.id


class Voortgang(models.Model):
    status = models.CharField(max_length=128) #online, optie, bij notaris, ...
    def __str__(self):
        return self.id

class Toegangslevel(models.Model):
    toegangslevelnaam = models.CharField(max_length=255)
    def __str__(self):
        return self.toegangslevelnaam


class Stad(models.Model):
    postcode = models.SmallIntegerField()
    stadsnaam = models.CharField(max_length=128)
    def __str__(self):
        return self.stadsnaam

class Gebruiker(AbstractBaseUser):
    #Id implemented by django
    voornaam = models.CharField(max_length=128)
    naam =  models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    straatnaam = models.CharField(max_length=128)
    huisnr = models.IntegerField()
    postcode = models.ForeignKey(Stad)
    busnr = models.CharField(max_length=10,  blank=True)
    telefoonnr = models.IntegerField()
    REQUIRED_FIELDS = ['voornaam', 'naam', 'email', 'postcode', 'telefoonnr']

    def __str__(self):
        return self.id

class Log(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    gebruiker = models.ForeignKey(Gebruiker)
    logText = models.CharField(max_length=255)

    def __str__(self):
        return self.id



class Pand(models.Model):
    #id autocreated by django
    gebruiker = models.ForeignKey(Gebruiker)
    straatnaam = models.CharField(max_length=128)
    huisnr = models.SmallIntegerField()
    postcodeID = models.ForeignKey(Stad)
    pandtype = models.ForeignKey(PandType)
    handelstatus = models.ForeignKey(Handelstatus)
    voortgang = models.ForeignKey(Voortgang)

    def __str__(self):
        return self.id


class Tag(models.Model):
    #id autocreated by django
    tagnaam = models.CharField(max_length=128)
    Pand = models.ManyToManyField(Pand)

    def __str__(self):
        return self.id



class Foto(models.Model):
    url = models.CharField(max_length=255)
    pand = models.ManyToManyField(Pand)

    def __str__(self):
        return self.id
