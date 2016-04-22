from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django import forms
from django.core.context_processors import csrf #websecurity crosside request reforgery
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
def partners(request):

	return render(request, 'webapp/partners.html')

def sander(request):
	if request.method == "POST":
		form = Stad(request.POST)
		if form.is_valid():
			model_instance = form.save(commit=False)
			model_instance.save()
			return redirect('index')
	else:
			form = Stad()
	return render(request, "webapp/sander.html", {'form': form})

def register(request):
	if request.method == "POST":
		form = Gebruiker(request.POST)
		if form.is_valid():
			model_instance = form.save(commit=False)
			model_instance.save()
			return redirect('index')
	else:
			form = Gebruiker()
	return render(request, "webapp/register.html", {'form': form})
#authentication-------------------------------------
def login(request):
	c= {}
	c.update(csrf(request))
	return render_to_response('webapp/login.html', c)

	#return render(request, 'webapp/login.html')

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/loggedin')
    else:
        return HttpResponseRedirect('/invalid')

def loggedin(request):
    return render_to_response('loggedin.html',
                              {'full_name': request.user.username})

def invalid_login(request):
    return render_to_response('invalid_login.html')

def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')
