from django import forms
from django.forms import ModelForm
from webapp.models import Stad
from webapp.models import User
from django.contrib import admin

class Stad(forms.ModelForm):
	class Meta:
		model = Stad
		fields = ['postcode', 'stadsnaam',]

class RegistrationForm(forms.ModelForm):
    """
    Form for registering a new account.
    """
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Password")
    password2 = forms.CharField(label="Password (again)")

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
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Paswoord'}))

    class Meta:
        fields = ['email', 'password']

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )

class PersonAdmin(admin.ModelAdmin):
    exclude = ['docfile']
    form = DocumentForm
