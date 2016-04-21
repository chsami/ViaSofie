from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms

from webapp.forms import Stad
from webapp.forms import Gebruiker
# Create your views here.
def index(request):
	return render(request, 'webapp/index.html')

def about(request):
	return render(request, 'webapp/about.html')

def contact(request):
	return render(request, 'webapp/contact.html')

def advies(request):
	return render(request, 'webapp/advies.html')

def huren(request):
	return render(request, 'webapp/huren.html')

def kopen(request):
	return render(request, 'webapp/kopen.html')

def login(request):
	return render(request, 'webapp/login.html')

def partners(request):
	return render(request, 'webapp/partners.html')

def sander(request):
	if request.method == "POST":
		form = Gebruiker(request.POST)
		if form.is_valid():
			model_instance = form.save(commit=False)
			model_instance.save()
			return redirect('index')
	else:
			form = Gebruiker()
	return render(request, "webapp/sander.html", {'form': form})
