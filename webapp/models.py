from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import uuid, random, hashlib
from django.db.models.signals import post_save, post_init

from datetime import datetime

def get_referentienummer():
    while True:
        currentYear = datetime.now().year
        referentienummer = str(currentYear) + "-" + str(uuid.uuid4())[:5]
        if not Pand.objects.filter(referentienummer=referentienummer).exists():
            return referentienummer.upper()

class Handelstatus(models.Model):
    status = models.CharField(max_length=128) #te koop, te huur

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

    activation_key = models.CharField(max_length=128, null=True, blank=True)
    key_expires = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    straatnaam = models.CharField(max_length=128)
    huisnr = models.CharField(max_length=10)
    busnr = models.CharField(max_length=10, null=True, blank=True)

    postcode = models.CharField(max_length=50)
    plaats = models.CharField(max_length=128)

    telefoonnr = models.CharField(max_length=128)

    objects = BaseUserManager()

    REQUIRED_FIELDS = ['voornaam', 'naam', 'postcode', 'plaats', 'telefoonnr', ]

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
    user = models.ForeignKey(User, blank=True, null=True)

    referentienummer = models.CharField(unique=True, default=get_referentienummer, editable=False, max_length=10)

    prijs = models.DecimalField(default=0, max_digits=18, decimal_places=0)
    slaapkamers = models.DecimalField(default=1, max_digits=10, decimal_places=0)
    badkamers = models.DecimalField(default=1, max_digits=10, decimal_places=0)
    parkeerplaats = models.BooleanField(default= False)

    handelstatus = models.ForeignKey(Handelstatus)
    voortgang = models.ForeignKey(Voortgang)
    uitgelicht = models.BooleanField(default= False)

    straatnaam = models.CharField(max_length=128)
    huisnr = models.SmallIntegerField()
    busnr = models.CharField(max_length=10, null=True, blank=True)
    postcode = models.CharField(max_length=50)
    plaats = models.CharField(max_length=128)

    beschrijving = models.TextField()
    beschrijving_2 = models.TextField(null=True, blank=True)

    review = models.TextField(null=True, blank=True)

    objects = models.Manager()

    def pandDetails(self):
        pand_pand_details = PandPandDetail.objects.filter(pand=self)
        return pand_pand_details

    def pandEPCs(self):
        pand_pand_epcs = PandPandEPC.objects.filter(pand=self)
        return pand_pand_epcs

    def pandDocuments(self):
        pand_pand_documents = PandPandDocument.objects.filter(pand=self)
        return pand_pand_documents

    def pandVoortgang(self):
        pand_pand_voortgang = Voortgang.objects.filter(pand=self)
        return pand_pand_voortgang

    @staticmethod
    def post_save(sender, **kwargs):
        instance = kwargs.get('instance')
        created = kwargs.get('created')

        bodh_users = BlijfOpDeHoogteUser.objects.all()
        try:
            bodh_users = bodh_users.filter(min_prijs <= instance.prijs)
        except Exception as e:
            pass

        try:
            bodh_users = bodh_users.filter(max_prijs >= instance.prijs)
        except Exception as e:
            pass

        if bodh_users:
            for bodh_user in bodh_users:
                print (bodh_user)

    def __str__(self):
        if self.user:
            return str(self.referentienummer) + " | " + str(self.user.naam) + " " + str(self.user.voornaam) + " | " + str(self.user.email)
        else:
            return str(self.referentienummer)

post_save.connect(Pand.post_save, sender=Pand)

class PandDetail(models.Model):
    #id autocreated by django
    naam = models.CharField(max_length=128)
    waarde = models.CharField(max_length=128, null=True, blank=True)

    

    def __str__(self):
        return str(self.naam) + ': ' + str(self.waarde)
#tussenrelatie
class PandPandDetail(models.Model):
    pand = models.ForeignKey(Pand)
    detail = models.ForeignKey(PandDetail, on_delete=models.CASCADE)

class PandEPC(models.Model):
    #id autocreated by django
    naam = models.CharField(max_length=128)
    waarde = models.CharField(max_length=128)

    def __str__(self):
        return str(self.naam) + ': ' + str(self.waarde)

class PandPandEPC(models.Model):
    pand = models.ForeignKey(Pand)
    epc = models.ForeignKey(PandEPC, on_delete=models.CASCADE)

class Foto(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d', blank=True)
    thumbnail = models.BooleanField(default= False)

    pand = models.ForeignKey(Pand)

    def __str__(self):
        return str(self.pand.referentienummer) + " - " + str(self.id)

class PandDocument(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d', blank=True)
    naam = models.CharField(max_length=256)
    plan = models.BooleanField(default=False)

    def __str__(self):
        return str(self.naam) + " - " + str(self.id)

class PandPandDocument(models.Model):
    pand = models.ForeignKey(Pand)
    document = models.ForeignKey(PandDocument, on_delete=models.CASCADE)

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

class StatusBericht(models.Model):
    titel = models.CharField(max_length=255)
    inhoud = models.TextField(max_length=1000)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.user.email) + " - " + str(self.titel)

class Data(models.Model):
    titel = models.CharField(max_length=255)
    data = models.TextField()

class BlijfOpDeHoogteUser(models.Model):
    voornaam = models.CharField(max_length=128)
    naam =  models.CharField(max_length=128)
    email = models.CharField(max_length=128, unique=True)
    telefoonnummer = models.CharField(max_length=128)

    straatnaam = models.CharField(max_length=128)
    huisnr = models.CharField(max_length=10)
    plaats = models.CharField(max_length=10, null=True, blank=True)
    postcode = models.CharField(max_length=50)

    min_prijs = models.DecimalField(null=True, blank=True, max_digits=18, decimal_places=0)
    max_prijs = models.DecimalField(null=True, blank=True, max_digits=18, decimal_places=0)

    REQUIRED_FIELDS = ['voornaam', 'naam', 'email', 'telefoonnummer', 'straatnaam', 'huisnr', 'plaats', 'postcode', ]

    def __str__(self):
        return str(self.voornaam) + " " + str(self.naam) + " - " + str(self.email)
