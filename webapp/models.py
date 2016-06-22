from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import uuid, random, hashlib

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

    activation_key = models.CharField(max_length=40, null=True, blank=True)
    key_expires = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    straatnaam = models.CharField(max_length=128)
    huisnr = models.CharField(max_length=10)
    postcode = models.ForeignKey(Stad)
    busnr = models.CharField(max_length=10, null=True, blank=True)

    telefoonnr = models.IntegerField()

    objects = BaseUserManager()

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

    referentienummer = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    straatnaam = models.CharField(max_length=128)
    huisnr = models.SmallIntegerField()
    busnr = models.CharField(max_length=10, null=True, blank=True)
    postcodeID = models.ForeignKey(Stad)
    handelstatus = models.ForeignKey(Handelstatus)
    voortgang = models.ForeignKey(Voortgang)
    beschrijving = models.TextField()
    uitgelicht = models.BooleanField(default= False)
    prijs = models.DecimalField(default=0, max_digits=18, decimal_places=2)
    thumbnail_url = models.CharField(max_length=256, null=True, blank=True)
    oppervlakte = models.CharField(max_length=256, null=True, blank=True)
    bouwjaar = models.SmallIntegerField()
    objects = models.Manager()

    def __str__(self):
        return str(self.referentienummer).replace('-', '') + " - " + str(self.postcodeID.postcode) + " " + str(self.postcodeID.stadsnaam) + ", " + str(self.straatnaam) + " " + str(self.huisnr) + " - " + str(self.user.email)


class Tag(models.Model):
    #id autocreated by django
    tagnaam = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.tagnaam

class TagPand(models.Model):
    tag = models.ForeignKey(Tag)
    pand = models.ForeignKey(Pand)
    value = models.CharField(max_length=255, default=1)

    def __str__(self):
        return str(self.pand.referentienummer).replace('-', '') + " - " + str(self.tag.tagnaam) + " (" + str(self.value) + ")"

class Foto(models.Model):
    url = models.CharField(max_length=255, null=True, blank=True)
    thumbnail = models.BooleanField(default= False)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d', blank=True)
    pand = models.ForeignKey(Pand)

    def __str__(self):
        return str(self.pand.referentienummer).replace('-', '') + " - " + str(self.id)

class Ebook(models.Model):
    naam = models.CharField(max_length=255)
    voornaam = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.email

class Faq(models.Model):
    titel = models.CharField(max_length=128)
    content = models.TextField()

    def __str__(self):
        return self.titel

class Partner(models.Model):
    naam = models.CharField(max_length=128)
    onderschrift = models.CharField(max_length=255)
    foto_url =  models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100,)
    link = models.CharField(max_length = 255)

class GoedDoel(models.Model):
    naam = models.CharField(max_length=128)
    bijschrift = models.CharField(max_length=500)
    link = models.CharField(max_length=255)
    foto_url = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100,)

    def __str__(self):
        return str(self.naam)

class PandReview(models.Model):
    """docstring for PandReview"""
    titel = models.CharField(max_length=128)
    auteur = models.CharField(max_length=128)
    text = models.CharField(max_length=500)
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )
    rating = models.CharField(max_length=2, choices=RATING_CHOICES, default=5)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(User, self).save(*args, **kwargs)

class StatusBericht(models.Model):
    titel = models.CharField(max_length=255)
    inhoud = models.TextField(max_length=1000)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.user.email) + " - " + str(self.titel)

class Data(models.Model):
    titel = models.CharField(max_length=255)
    data = models.TextField()
