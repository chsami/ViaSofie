from django import forms
from django.forms import ModelForm
from webapp.models import Stad

class Stad(forms.ModelForm):
	class Meta:
		model = Stad
		fields = ['postcode', 'stadsnaam',]

