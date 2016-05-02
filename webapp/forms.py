from django import forms
from django.forms import ModelForm
from webapp.models import Stad
from webapp.models import Gebruiker
from webapp.models import Ebook
from webapp.models import PandType
from webapp.models import Handelstatus
from webapp.models import Voortgang
from webapp.models import Toegangslevel
from webapp.models import *


class Stad(forms.ModelForm):
	class Meta:
		model = Stad
		fields = ['postcode', 'stadsnaam',]


class Ebookform(forms.ModelForm):
	class Meta:
		model = Ebook
		fields = ['naam', 'voornaam', 'email',]


class PandType(forms.ModelForm):
	class Meta:
		model = PandType
		fields = ['pandtype',]

class Handelstatus(forms.ModelForm):
	class Meta:
		model = Handelstatus
		fields = ['status',]


class Voortgang(forms.ModelForm):
	class Meta:
		model = Voortgang
		fields = ['status',]

class Toegangslevel(forms.ModelForm):
	class Meta:
		model = Toegangslevel
		fields = ['toegangslevelnaam',]



class Pand(forms.ModelForm):
	class Meta:
		model = Pand
		fields = ['gebruiker', 'straatnaam', 'huisnr', 'postcode', 'pandtype', 'handelstatus', 'voortgang',]


class Tag(forms.ModelForm):
	class Meta:
		model = Tag
		fields = ['tagnaam', 'pand',]

class Log(forms.ModelForm):
	class Meta:
		model = Log
		fields = ['gebruiker', 'logText',]
		exclude = ['created',]


class Foto(forms.ModelForm):
	class Meta:
		model = Foto
		fields = ['url', 'pand']