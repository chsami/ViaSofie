from django.db import models


# Create your models here.
class Gebruiker(models.Model):
    #userid = models.Autofield(primary_key=True)
    voornaam = models.charField(max_length=50)
    naam =  models.charField(max_length=50)
    email = models.charField(max_length=50)
    straatnaam = models.charField(max_length=50)
    huisnr = models.IntegerField()
    postcode = models.IntegerField()
    busnr = models.charField(max_length=10)
    telefoonnr = models.IntegerField()
    password= models.charField(max_length=30) #ToDo: add hashes + saltes (import)
    toegangslevel = models.ForeignKey(Toegangslevel, on_delete=models.CASCADE)

    def __str__(self):              # __unicode__ on Python
        return self.name
        #authentication https://docs.djangoproject.com/en/1.9/topics/auth/customizing/



class TblUserLog(models.Model)
    created = models.DateTimeField(auto_now_add=True)
    gebruiker = models.ForeignKey(Gebruiker, on_delete=models.CASCADE)
    tbllog = models.ForeignKey(TblLog, on_delete= models.CASCADE)


class TblLog(models.Model)
    logText = models.charField(255)
    tblUserLogs = models.ManytoManyField(Gebruiker, through="TblUserLogs")

 class Toegangslevel
    toegangslevelnaam = models.charField(255)
