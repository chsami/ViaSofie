from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.core.urlresolvers import reverse
from django import forms
from webapp.models import Foto
from webapp.forms import Stad, User, AuthenticationForm, RegistrationForm, FotoForm
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

# def list(request):
#     # Handle file upload
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
# 		if form.is_valid():
#             newdoc = Document(docfile=request.FILES['docfile'])
#             newdoc.save()
#
#             # Redirect to the document list after POST
#             return HttpResponseRedirect(reverse('list'))
#     else:
#         form = DocumentForm()  # A empty, unbound form
#
#     # Load documents for the list page
#     documents = Document.objects.all()
#
#     # Render list page with the documents and the form
#     return render(
#         request,
#         'webapp/list.html',
#         {'documents': documents, 'form': form}
#     )


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

	# Load documents for the list page
	documents = Foto.objects.all()

	# Render list page with the documents and the form
	return render(
		request,
		'webapp/foto.html',
		{'documents': documents, 'form': form}
	)
