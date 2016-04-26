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


class Stad(models.Model):
    postcode = models.SmallIntegerField()
    stadsnaam = models.CharField(max_length=128)
    def __str__(self):
        return self.stadsnaam

class User(AbstractBaseUser):
    #Id implemented by django
    USERNAME_FIELD = 'email'

    voornaam = models.CharField(max_length=128)
    naam =  models.CharField(max_length=128)
    email = models.CharField(max_length=128, unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    straatnaam = models.CharField(max_length=128)
    huisnr = models.IntegerField()
    postcode = models.ForeignKey(Stad)
    busnr = models.CharField(max_length=10,  blank=True)

    telefoonnr = models.IntegerField()

    REQUIRED_FIELDS = ['voornaam', 'naam', 'postcode', 'telefoonnr', ]

    def __str__(self):
        return self.email

class Log(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    logText = models.CharField(max_length=255)

    def __str__(self):
        return self.id



class Pand(models.Model):
    #id autocreated by django
    user = models.ForeignKey(User)
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