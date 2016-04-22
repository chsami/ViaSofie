from django import forms
from django.forms import ModelForm
from webapp.models import Stad
from webapp.models import Gebruiker

class Stad(forms.ModelForm):
	class Meta:
		model = Stad
		fields = ['postcode', 'stadsnaam',]


class Gebruiker(forms.ModelForm):
	class Meta:
		model = Gebruiker
		fields = ['voornaam', 'naam', 'email', 'straatnaam', 'huisnr', 'postcode', 'busnr', 'toegangslevel', 'telefoonnr', 'password', ]

class Ebook(forms.ModelForm):
	class Meta:
		model = Ebook
		fields = ['naam', 'voornaam', 'email',]