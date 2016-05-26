from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.core.urlresolvers import reverse
from django import forms
from django.shortcuts import render, redirect, render_to_response, RequestContext, get_object_or_404
from django.db import models
from webapp.models import *
from webapp.models import Pand as PandModel
from webapp.models import Foto as FotoModel
from webapp.models import Faq as FaqModel
from webapp.models import Partner as PartnerModel
from django.utils.translation import ugettext as _
from webapp.forms import *
import hashlib
import random
from django.utils import timezone
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def languageselector(request):
    if request.method == 'POST':
        languager = form.cleaned_data['language.code']
        path = 'webapp/locale/' + languager + '/LC_MESSAGES/django.po'
        lines = tuple(open(filename, 'r'))
        for line in lines:
            if(line.startswith("#: webapp/templates/admin/index.html") ):
                i = 1
                while(i != 3):
                    output = lines[line+i]
                    i += 1

        return render_to_response('webapp/languageselector.html', {'lines': output})


        # filepath = os.path.join(BASE_DIR, path)
        # file = open('filepath', 'r')
        # base = file.read()
        # file.close()
        # link = form.cleaned_data['url']

        # lines = tuple(open(filename, 'r'))
        # lines = tuple(open('webapp/locale/nl/LC_MESSAGES/django.po', 'r'))
        # with open(fname) as f:
        #     content = f.readlines()

        #edit file here
        # for line in open('base'):
        #     if(line == "#: webapp/templates/admin/index.html")



        # file = open(filepath, 'w')
        # file.write(puzzleSolution)
        # file.close()



    return render(request, 'webapp/languageselector.html')


def index(request):
    return render(request, 'webapp/index.html')


def panddetail(request, pand_referentienummer):
	pand = PandModel.objects.get(referentienummer=pand_referentienummer)
	fotos = FotoModel.objects.filter(pand_id=pand.id)
	return render_to_response('webapp/pand.html', {'pand': pand, 'fotos': fotos})

def about(request):
	return render(request, 'webapp/about.html')

def panden(request):
    context = {
        'panden': PandModel.objects.all(),
        'panden_item': 'webapp/panden_item.html',
    }
    template = 'webapp/panden.html'
    if request.is_ajax():
        template = 'webapp/panden_item.html'
    return render_to_response(template, context, context_instance=RequestContext(request))

def contact(request):
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['email']
            name = form.cleaned_data['name']
            fullmessage = "name: " + name + "\tmessage:"+ message
            try:
                send_mail(subject, fullmessage, sender, ['liekensjeff@gmail.com'])
            except BadHeaderError:
                return HttpResponse("invalid.")

            # template = get_template('contact_template.txt')
            # context = Context({
            #     'contact_email': sender,
            #     'contact_name': name,
            #     'subject': subject,
            #     'form_content': message,
            # })
            #
            # content = template.render(context)
            # content = template.render(context)

            # to = 'liekensjeff@gmail.com'
            # send_mail(subject, message, sender, to, fail_silently=False )
	form = ContactForm()
    return render_to_response('webapp/contact.html', {
	   'form': form,
	}, context_instance=RequestContext(request))


def advies(request):
	faq_list = FaqModel.objects.all()
	return render_to_response('webapp/advies.html', {'faq_list': faq_list})

def account(request):
    faq_list = FaqModel.objects.all()
    return render_to_response('webapp/account.html', {'faq_list': faq_list})

def huren(request):
	return render(request, 'webapp/huren.html')

def kopen(request):
	return render(request, 'webapp/kopen.html')

def forms(request):
	return render(request, 'webapp/forms.html')

def referenties(request):
	return render(request, 'webapp/referenties.html')

def disclaimer(request):
	return render(request, 'webapp/disclaimer.html')

def privacy(request):
    return render(request, 'webapp/privacy.html')

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

def loginpopup(request):
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
	return render_to_response('webapp/loginpopup.html', {
		'form': form,
	}, context_instance=RequestContext(request))

def partners(request):
	partner_list = PartnerModel.objects.all()
	return render_to_response('webapp/partners.html', {'partner_list': partner_list})

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

# def pand(request):
# 	if request.method == "POST":
# 		form = Pand(request.POST)
# 		if form.is_valid():
# 			model_instance = form.save(commit=False)
# 			model_instance.save()
# 			return redirect('formsucces')
# 	else:
# 			form = Pand()
# 	return render(request, "webapp/forms.html", {'form': form})

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
    if request.user.is_authenticated():
        return redirect('/')
    registration_form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            datas={}
            datas['email']=form.cleaned_data['email']
            datas['password1']=form.cleaned_data['password1']

            #We will generate a random activation key
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            emailsalt = datas['email']
            if isinstance(emailsalt, unicode):
                emailsalt = emailsalt.encode('utf8')
            datas['activation_key']= hashlib.sha1(salt+emailsalt).hexdigest()

            datas['email_path']="/ActivationEmail.py"
            datas['email_subject']="Welkom bij ViaSofie"

            form.sendEmail(datas) #Send validation email
            form.save(datas) #Save the user and his profile

            request.session['registered']=True #For display purposes
            return redirect('/')
        else:
            registration_form = form #Display form with error messages (incorrect fields, etc)
    else:
    	form = RegistrationForm()
    return render(request, 'webapp/register.html', locals())

#View called from activation email. Activate user if link didn't expire (48h default), or offer to
#send a second link if the first expired.
def activation(request, key):
    activation_expired = False
    already_active = False
    user = get_object_or_404(User, activation_key=key)
    if user.is_active == False:
        if timezone.now() > user.key_expires:
            activation_expired = True #Display : offer to user to have another activation link (a link in template sending to the view new_activation_link)
            id_user = user.id
        else: #Activation successful
            user.is_active = True
            user.save()

    #If user is already active, simply display error message
    else:
        already_active = True #Display : error message
    return render(request, 'webapp/activation.html', locals())

def new_activation_link(request, user_id):
    form = RegistrationForm()
    datas={}
    user = User.objects.get(id=user_id)
    if user is not None and not user.is_active:
        datas['username']=user.username
        datas['email']=user.email
        datas['email_path']="/ResendEmail.py"
        datas['email_subject']="Jou nieuwe activatielink bij ViaSofie"

        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        usernamesalt = datas['username']
        if isinstance(usernamesalt, unicode):
            usernamesalt = usernamesalt.encode('utf8')
        datas['activation_key']= hashlib.sha1(salt+usernamesalt).hexdigest()

        user = User.objects.get(user=user)
        user.activation_key = datas['activation_key']
        user.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        user.save()

        form.sendEmail(datas)
        request.session['new_link']=True #Display : new link send

    return redirect('/')

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

# EDIT VIEWS
def panddetail_edit(request, pand_referentienummer):
	pand = PandModel.objects.get(referentienummer=pand_referentienummer)
	fotos = FotoModel.objects.filter(pand_id=pand.id)
	return render_to_response('webapp/edit/pand.html', {'pand': pand, 'fotos': fotos})
