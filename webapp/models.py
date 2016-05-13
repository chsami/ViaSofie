from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin



class PandType(models.Model):
    pandtype = models.CharField(max_length=128) #kantoor,huis, appartement, ...

    def __str__(self):
        return self.pandtype


class Handelstatus(models.Model):
    status = models.CharField(max_length=128) #verkoop, verhuur, verpachten, ...

    def __str__(self):
        return self.status


class Voortgang(models.Model):
    status = models.CharField(max_length=128) #online, optie, bij notaris, ...
    def __str__(self):
        return self.status


class Stad(models.Model):
    postcode = models.CharField(max_length= 12)
    stadsnaam = models.CharField(max_length=128)

    def __str__(self):
        return self.stadsnaam

    def new_stad(self, postcode, stadsnaam):
        self.postcode = postcode
        self.stadsnaam = stadsnaam

class User(AbstractBaseUser, PermissionsMixin):
    #Id implemented by django
    USERNAME_FIELD = 'email'

    voornaam = models.CharField(max_length=128)
    naam =  models.CharField(max_length=128)
    email = models.CharField(max_length=128, unique=True)

    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    straatnaam = models.CharField(max_length=128)
    huisnr = models.IntegerField()

    postcode = models.ForeignKey(Stad)

    busnr = models.CharField(max_length=10, null=True, blank=True)

    objects = BaseUserManager()

    telefoonnr = models.IntegerField()

    REQUIRED_FIELDS = ['voornaam', 'naam', 'postcode', 'telefoonnr', ]

    def __str__(self):
        return self.email

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Log(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    logText = models.CharField(max_length=255)

    def __str__(self):
        return self.logText


class Pand(models.Model):
    #id autocreated by django
    user = models.ForeignKey(User)
    straatnaam = models.CharField(max_length=128)
    huisnr = models.SmallIntegerField()
    busnr = models.CharField(max_length=10, null=True, blank=True)
    postcodeID = models.ForeignKey(Stad)
    pandtype = models.ForeignKey(PandType)
    handelstatus = models.ForeignKey(Handelstatus)
    voortgang = models.ForeignKey(Voortgang)

    def __str__(self):
        return str(self.id)


class Tag(models.Model):
    #id autocreated by django
    tagnaam = models.CharField(max_length=128)
    pand = models.ManyToManyField(Pand)

    def __str__(self):
        return self.tagnaam

class Foto(models.Model):
    url = models.CharField(max_length=255)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d', blank=True)
    pand = models.ManyToManyField(Pand)

    def __str__(self):
        return str(self.id)

class Ebook(models.Model):
    naam = models.CharField(max_length=255)
    voornaam = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.id
