from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.core.urlresolvers import reverse
from django import forms
from django.shortcuts import render, redirect, render_to_response, RequestContext
from django.db import models
from webapp.models import *
from webapp.forms import *

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

def forms(request):
	return render(request, 'webapp/forms.html')

def login(request):
	"""
    Log in view
    """
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = authenticate(email=request.POST['email'], password=request.POST['password'])
			if user is not None:
				if user.is_active:
					django_login(request, user)
					return redirect('/')
	else:
		form = AuthenticationForm()
	return render_to_response('webapp/login.html', {
		'form': form,
	}, context_instance=RequestContext(request))

def partners(request):
	return render(request, 'webapp/partners.html')
def formsucces(request):
	return render(request, 'webapp/formsucces.html')


def stad(request):
	if request.method == "POST":
		form = Stad(request.POST)
		if form.is_valid():
			model_instance = form.save(commit=False)
			model_instance.save()
			return redirect('formsucces')
	else:
			form = Stad()
	return render(request, "webapp/forms.html", {'form': form})

def ebooks(request):
	if request.method == "POST":
		form = Ebookform(request.POST)
		if form.is_valid():
			model_instance = form.save(commit=False)
			model_instance.save()
			return redirect('ebook_lijst')
	else:
			form = Ebookform()
	return render(request, "webapp/forms.html", {'form': form})

def ebook_lijst(request):
	ebooks = Ebook.objects.all()
  	ebook_data = {
  	"ebook_detail" : ebooks
  	}

  	return render_to_response('webapp/ebook_lijst.html', ebook_data, context_instance=RequestContext(request))


def pandtype(request):
	if request.method == "POST":
		form = PandType(request.POST)
		if form.is_valid():
			model_instance = form.save(commit=False)
			model_instance.save()
			return redirect('formsucces')
	else:
			form = PandType()
	return render(request, "webapp/forms.html", {'form': form})

def handelstatus(request):
	if request.method == "POST":
		form = Handelstatus(request.POST)
		if form.is_valid():
			model_instance = form.save(commit=False)
			model_instance.save()
			return redirect('formsucces')
	else:
			form = Handelstatus()
	return render(request, "webapp/forms.html", {'form': form})


def voortgang(request):
	if request.method == "POST":
		form = Voortgang(request.POST)
		if form.is_valid():
			model_instance = form.save(commit=False)
			model_instance.save()
			return redirect('formsucces')
	else:
			form = Voortgang()
	return render(request, "webapp/forms.html", {'form': form})

def pand(request):
	if request.method == "POST":
		form = Pand(request.POST)
		if form.is_valid():
			model_instance = form.save(commit=False)
			model_instance.save()
			return redirect('formsucces')
	else:
			form = Pand()
	return render(request, "webapp/forms.html", {'form': form})

def tag(request):
	if request.method == "POST":
		form = Tag(request.POST)
		if form.is_valid():
			model_instance = form.save(commit=False)
			model_instance.save()
			return redirect('formsucces')
	else:
			form = Tag()
	return render(request, "webapp/forms.html", {'form': form})

def log(request):
	if request.method == "POST":
		form = Log(request.POST)
		if form.is_valid():
			model_instance = form.save(commit=False)
			model_instance.save()
			return redirect('formsucces')
	else:
			form = Log()
	return render(request, "webapp/forms.html", {'form': form})

def register(request):
    """
    User registration view.
    """
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/')
    else:
        form = RegistrationForm()
    return render_to_response('webapp/register.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def logout(request):
    """
    Log out view
    """
    django_logout(request)
    return redirect('/')

def foto(request):
	# Handle file upload
	if request.method == 'POST':
		form = FotoForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = Foto(docfile=request.FILES['docfile'])
			newdoc.save()

			# Redirect to the document list after POST
			return HttpResponseRedirect(reverse('list'))
	else:
		form = FotoForm()  # A empty, unbound form

	# Render list page with the documents and the form
	return render(
		request,
		'webapp/foto.html',
		{'form': form}
	)