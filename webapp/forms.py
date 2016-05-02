from django import forms
from django.forms import ModelForm
from webapp.models import Stad
<<<<<<< HEAD
from webapp.models import User
from django.contrib import admin
=======
from webapp.models import Gebruiker
from webapp.models import Ebook
from webapp.models import PandType
from webapp.models import Handelstatus
from webapp.models import Voortgang
from webapp.models import Toegangslevel
from webapp.models import *

>>>>>>> refs/remotes/origin/Sander

class Stad(forms.ModelForm):
	class Meta:
		model = Stad
		fields = ['postcode', 'stadsnaam',]

class RegistrationForm(forms.ModelForm):
    """
    Form for registering a new account.
    """
<<<<<<< HEAD
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label="Wachtwoord", widget=forms.PasswordInput(attrs={'placeholder': 'Paswoord'}))
    password2 = forms.CharField(label="Wachtwoord (opnieuw)", widget=forms.PasswordInput(attrs={'placeholder': 'Paswoord'}))
    voornaam = forms.CharField(label="Voornaam", widget=forms.TextInput(attrs={'placeholder': 'Voornaam'}))
    naam = forms.CharField(label="Naam", widget=forms.TextInput(attrs={'placeholder': 'Naam'}))
    straatnaam = forms.CharField(label="Straatnaam", widget=forms.TextInput(attrs={'placeholder': 'Straatnaam'}))
    huisnr = forms.CharField(label="Huisnummer", widget=forms.NumberInput(attrs={'placeholder': 'Bijv: 1'}))
    postcode = forms.CharField(label="Postcode", widget=forms.TextInput(attrs={'placeholder': 'Bijv: 2000'}))
    busnr = forms.CharField(label="Busnummer", widget=forms.NumberInput(attrs={'placeholder': 'Bijv: 1'}))
    telefoonnr = forms.CharField(label="Telefoonnummer", widget=forms.TextInput(attrs={'placeholder': 'Telefoonnr'}))
=======
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Wachtwoord")
    password2 = forms.CharField(label="Wachtwoord (nogmaals)")
>>>>>>> refs/remotes/origin/TinneOrigin

<<<<<<< HEAD
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'voornaam', 'naam', 'straatnaam', 'huisnr', 'postcode', 'busnr', 'telefoonnr', ]

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class AuthenticationForm(forms.Form):
    """
    Login form
    """
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Wachtwoord'}))

    class Meta:
        fields = ['email', 'password']

class FotoForm(forms.Form):

	# class Meta:
	# 	model: Foto
	# 	fields['docfile']
	docfile = forms.FileField(
		label='Select a file'
	)
=======
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
>>>>>>> refs/remotes/origin/Sander
