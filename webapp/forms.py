from django import forms
from django.forms import ModelForm
from django.contrib import admin
from webapp.models import *
from captcha.fields import ReCaptchaField
from django.template import Context, Template
from django.conf import settings
from django.core.mail import send_mail
import datetime

class PartnersForm(forms.ModelForm):
	naam = forms.CharField(label="Naam", widget=forms.TextInput(attrs={'placeholder': 'Naam'}))
	onderschrift = forms.CharField(label="Onderschrift", widget=forms.TextInput(attrs={'placeholder': 'Onderschrift'}))
	foto_url = forms.CharField(label="foto_url", widget=forms.TextInput(attrs={'placeholder': 'foto_url'}))
	class Meta:
		model = Partner
		fields = ['naam', 'onderschrift', 'foto_url',]

class Stad(forms.ModelForm):
	class Meta:
		model = Stad
		fields = ['postcode', 'stadsnaam',]

class RegistrationForm(forms.ModelForm):
    """
    Form for registering a new account.
    """
    email = forms.EmailField(label="*E-mail", widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    password1 = forms.CharField(label="*Wachtwoord", widget=forms.PasswordInput(attrs={'placeholder': 'Wachtwoord'}))
    password2 = forms.CharField(label="*Wachtwoord (nogmaals)", widget=forms.PasswordInput(attrs={'placeholder': 'Wachtwoord'}))
    voornaam = forms.CharField(label="*Voornaam", widget=forms.TextInput(attrs={'placeholder': 'Voornaam'}))
    naam = forms.CharField(label="*Naam", widget=forms.TextInput(attrs={'placeholder': 'Naam'}))
    straatnaam = forms.CharField(label="*Straatnaam", widget=forms.TextInput(attrs={'placeholder': 'Straatnaam'}))
    huisnr = forms.CharField(label="*Huisnummer", widget=forms.NumberInput(attrs={'placeholder': 'Bijv: 1'}))
    busnr = forms.CharField(required=False, label="Busnummer", widget=forms.NumberInput(attrs={'placeholder': 'Bijv: 1'}))
    telefoonnr = forms.CharField(label="*Telefoonnummer", widget=forms.TextInput(attrs={'placeholder': 'Telefoonnr'}))
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'voornaam', 'naam', 'straatnaam', 'huisnr', 'postcode', 'busnr', 'telefoonnr', 'captcha', ]

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

    def save(self, datas):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.activation_key=datas['activation_key']
        user.key_expires=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        user.save()
        return user

    #Handling of activation email sending ------>>>!! Warning : Domain name is hardcoded below !!<<<------
    #I am using a text file to write the email (I write my email in the text file with templatetags and then populate it with the method below)
    def sendEmail(self, datas):
        link='http://localhost:8000/activate/'+datas['activation_key']
        c=Context({'activation_link':link,'email':datas['email']})
        f = open(settings.MEDIA_ROOT+datas['email_path'], 'r')
        t = Template(f.read())
        f.close()
        message=t.render(c)
        #print unicode(message).encode('utf8')
        send_mail(datas['email_subject'], message, 'ViaSofie <viasofie.groep5@gmail.com>', [datas['email']], fail_silently=False)

class AuthenticationForm(forms.Form):
    """
    Login form
    """
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Wachtwoord'}))

    class Meta:
        fields = ['email', 'password']

class FotoForm(forms.Form):

	# class Meta:
	# 	model: Foto
	# 	fields['docfile']
	docfile = forms.FileField(
		label='Select a file'
	)

class Ebookform(forms.ModelForm):
	naam = forms.CharField(label="*Naam", widget=forms.TextInput(attrs={'placeholder': 'Naam'}))
	voornaam = forms.CharField(label="*Voornaam", widget=forms.TextInput(attrs={'placeholder': 'Voornaam'}))
	email = forms.EmailField(label="*E-mail", widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
	captcha = ReCaptchaField()

	class Meta:
		model = Ebook
		fields = ['naam', 'voornaam', 'email', 'captcha',]

class Handelstatus(forms.ModelForm):
	class Meta:
		model = Handelstatus
		fields = ['status',]

class Voortgang(forms.ModelForm):
	class Meta:
		model = Voortgang
		fields = ['status',]

class Pand(forms.ModelForm):
	class Meta:
		model = Pand
		fields = ['user', 'straatnaam', 'huisnr', 'postcodeID', 'handelstatus', 'voortgang',]

class Tag(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tagnaam']

class Log(forms.ModelForm):
	class Meta:
		model = Log
		fields = ['user', 'logText',]
		exclude = ['created',]

class Foto(forms.ModelForm):
	class Meta:
		model = Foto
		fields = ['url', 'pand']

# class ContactForm(forms.ModelForm):
# 	"""
#     Form for sending a mail via contactpage.
#     """
# 	email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'placeholder' : 'E-mail'}))
# 	naam = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Naam'}))
#     onderwerp = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder' : 'Onderwerp'}))
#     bericht = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Bericht'}))
#
#     class Meta:
#
# 	def sendEmail(self, datas):
#         link='http://localhost:8000/activate/'+datas['activation_key']
#         c=Context({'activation_link':link,'email':datas['email']})
#         f = open(settings.MEDIA_ROOT+datas['email_path'], 'r')
#         t = Template(f.read())
#         f.close()
#         message=t.render(c)
#         #print unicode(message).encode('utf8')
#         send_mail([datas['onderwerp']], [datas['bericht']], [datas['email']], '<liekensjeff@gmail.com>', fail_silently=False)

# https://docs.djangoproject.com/ja/1.9/topics/forms/
class ContactForm(forms.Form):
	name = forms.CharField( max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Naam'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
	subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Onderwerp'}))
	message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Bericht'}))
	captcha = ReCaptchaField()

class SearchForm(forms.Form):
    plaats_postcode_refnummer = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "search-form-input", id: "id_plaats_postcode", 'name': "plaats_postcode", 'placeholder': "Zoek op referentienummer, plaats of postcode", 'type': "text"}), required = False)
    # pand_type = forms.ChoiceField(widget=forms.Select(attrs={'id': 'pand-type', 'class': 'pand-type-input'}))
    kopen = forms.BooleanField(widget = forms.HiddenInput(attrs={'id': 'kopen_hiddenfield', 'value':'true'}))
    pand_type = forms.CharField(widget= forms.HiddenInput(attrs={'id': 'pand_type_hiddenfield', 'value':'Huis'}))
    prijsSliderKopen = forms.CharField(widget= forms.HiddenInput(attrs={'id': 'prijssliderkopen_hiddenfield', 'value':'15000,100000'}))
    prijsSliderHuren = forms.CharField(widget= forms.HiddenInput(attrs={'id': 'prijssliderhuren_hiddenfield', 'value':'1000,5000'}))
    tagsSearch = forms.CharField(widget= forms.HiddenInput(attrs={'id': 'prijssliderhuren_hiddenfield', 'value':''}))
    # prijs_range = forms.DecimalField(widget=forms.TextInput(attrs={'id': 'prijs-range','class': 'prijs-range-input', 'readonly style': ''}))
    # aantal_slaapkamers = forms.IntegerField(widget=forms.TextInput(attrs={'id': 'aantal-slaapkamers','class': 'aantal-slaapkamers-input', 'readonly style': ''}))
    # aantal_badkamers = forms.IntegerField(widget=forms.TextInput(attrs={'id': 'aantal-badkamers','class': 'aantal-badkamers-input', 'readonly style': ''}))
    # aantal_verdiepen = forms.IntegerField(widget=forms.TextInput(attrs={'id': 'aantal-verdiepen','class': 'aantal-verdiepen-input', 'readonly style': ''}))
    # tags = forms.CharField(label="", widget=forms.TextInput(attrs={'id': 'tags', 'data-role': 'tagsinput'}))

    class Meta:
        fields = ['plaats_postcode_refnummer', 'pand_type', 'aantal_slaapkamers', 'aantal_badkamers', 'aantal_verdiepen', 'prijs_range', 'tags']

class SmallSearchForm(forms.Form):
	kopen = forms.BooleanField(widget = forms.HiddenInput(attrs={'id': 'kopen_hiddenfield', 'Value': 'true'}), required = False)
	plaats_postcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'search-form-input', 'placeholder': 'Zoek op plaats of postcode'}), required = False)

	class Meta:
		fields = ['kopen', 'plaats_postcode']
