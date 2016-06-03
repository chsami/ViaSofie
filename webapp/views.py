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
from webapp.models import User as UserModel
from webapp.models import GoedDoel as GoedDoelModel
from webapp.models import TagPand as TagPandModel
from django.utils.translation import ugettext as _
from webapp.forms import *
import hashlib
import random
from django.utils import timezone
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

#sander is awesome
#removed 171 lines of code
def slogin(request):
    if request.method == 'POST' and 'loginbtn' in request.POST:
        formlogin = AuthenticationForm(data=request.POST)
        if formlogin.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                else:
                    return redirect("/login")
            else:
                return redirect("/login")
    else:
        formlogin=AuthenticationForm()
    return formlogin
# Create your views here.
def index(request):
    dpartners = Data.objects.get(id=11)
    formlogin = slogin(request)
    panden = PandModel.objects.filter(uitgelicht=True)
    panden_lijst = list(panden)
    uitgelichte_panden = []
    for i in range (0,3):
        if len(panden_lijst) > 0:
            uitgelichte_panden.append(panden_lijst.pop(random.randint(0, len(panden_lijst) -1)))
    # GOEDE DOELEN
    goede_doelen = GoedDoelModel.objects.all()
    #PARTNERS
    partner_list = PartnerModel.objects.all()
    return render_to_response('webapp/index.html', {'dpartners': dpartners, 'uitgelichte_panden': uitgelichte_panden, 'goede_doelen': goede_doelen, 'formlogin':formlogin, 'partner_list': partner_list}, context_instance=RequestContext(request))

def panddetail(request, pand_referentienummer):
    formlogin = slogin(request)
    pand = PandModel.objects.get(referentienummer=pand_referentienummer)
    #voeg extra gegevens toe
    relatedPands= PandModel.objects.filter(postcodeID=pand.postcodeID)
    fotos = FotoModel.objects.filter(pand_id=pand.id)

    # Tags van pand moeten op de volgende wijze worden megegeven: "Zwembad,Veranda,Tuin"
    tagpand_list = TagPandModel.objects.filter(pand_id=pand.id)
    tag_data = ""
    for tagpand in tagpand_list:
        tag_data += "%s (%s)," % (str(tagpand.tag), tagpand.value)
    # Laatste onnodige comma wordt weggehaald
    tag_data = tag_data[:-1]

    all_tagpand_list = TagPandModel.objects.all()

    all_tags = []
    temp_tag = ""
    for tagpand in all_tagpand_list:
        for i in range(0,20):
            temp_tag = "%s (%s)" % (str(tagpand.tag), str(i))
            all_tags.append(temp_tag)

    return render_to_response('webapp/pand.html', {'pand': pand, 'fotos' : fotos, 'relatedPands' : relatedPands, 'tag_data': tag_data, 'all_tags': all_tags, 'formlogin':formlogin}, context_instance=RequestContext(request))

def panden(request):
    data = Data.objects.get(id=13)
    formlogin = slogin(request)
    context = {
        'panden': PandModel.objects.all().values(),
        'panden_item': 'webapp/panden_item.html',
        'formlogin': formlogin,
        'data': data,
    }
    template = 'webapp/panden.html'
    if request.is_ajax():
        template = 'webapp/panden_item.html'
    return render_to_response(template, context, context_instance=RequestContext(request))

def referenties(request):
    data = Data.objects.get(id=9)
    formlogin = slogin(request)
    context = {
        # 'panden' = PandModel.objects.get(handelstatus='Verkocht',handelstatus='Verhuurd')
        'panden': PandModel.objects.all().values(),
        'panden_item': 'webapp/panden_item.html',
        'formlogin': formlogin,
        'data': data,
    }
    template = 'webapp/panden.html'
    if request.is_ajax():
        template = 'webapp/panden_item.html'
    return render_to_response(template, context, context_instance=RequestContext(request))

def account(request):
    formlogin = slogin(request)
    current_user = request.user
    if current_user.is_authenticated():
        # Do something for authenticated users.
        return render_to_response('webapp/account.html', {'current_user': current_user,'formlogin': formlogin }, context_instance=RequestContext(request))
    else:
        # Do something for anonymous users.
        return render_to_response('webapp/account.html', {'current_user': current_user, 'formlogin': formlogin}, context_instance=RequestContext(request))


def about(request):
    dabout = Data.objects.get(id=10)
    formlogin = slogin(request)
    return render_to_response('webapp/about.html', {'formlogin': formlogin, 'dabout': dabout}, context_instance=RequestContext(request))


def contact(request):
    dcontact = Data.objects.get(id=3)
    dadres = Data.objects.get(id=4)
    dtelefoon = Data.objects.get(id=5)
    dmail = Data.objects.get(id=6)
    if request.method == 'POST' and 'loginbtn' in request.POST:
        form = ContactForm()
        formlogin = AuthenticationForm(data=request.POST)
        if formlogin.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                else:
                    return redirect("/login")
            else:
                return redirect("/login")
    elif(request.method == 'POST'):
        formlogin = AuthenticationForm(data=request.POST)
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
        form = ContactForm()
    else:
        form = ContactForm()
        formlogin = AuthenticationForm()
            #====================voor template toe te voegen=========================
            # template = get_template('contact_template.txt')
            # context = Context({
            #     'contact_email': sender,
            #     'contact_name': name,
            #     'subject': subject,
            #     'form_content': message,
            # })
    return render_to_response('webapp/contact.html', {
        'form': form,
        'formlogin': formlogin,
        'dcontact' : dcontact,
        'dadres' : dadres,
        'dmail' : dmail,
        'dtelefoon' : dtelefoon,
        }, context_instance=RequestContext(request))

def advies(request):
    dadvies = Data.objects.get(id=8)
    dfaq = Data.objects.get(id=7)
    formlogin = slogin(request)
    faq_list = FaqModel.objects.all()
    return render_to_response('webapp/advies.html', {'dadvies': dadvies, 'dfaq': dfaq, 'faq_list': faq_list, 'formlogin': formlogin}, context_instance=RequestContext(request))

def huren(request):
    formlogin = slogin(request)
    return render_to_response('webapp/huren.html', {'formlogin': formlogin}, context_instance=RequestContext(request))

def kopen(request):
    formlogin = slogin(request)
    return render_to_response('webapp/kopen.html', {'formlogin': formlogin}, context_instance=RequestContext(request))

def disclaimer(request):
    data = Data.objects.get(id=1)
    formlogin = slogin(request)
    return render_to_response('webapp/disclaimer.html', {'formlogin': formlogin, 'data': data}, context_instance=RequestContext(request))

def privacy(request):
    data = Data.objects.get(id=2)
    formlogin = slogin(request)
    return render_to_response('webapp/privacy.html', {'formlogin': formlogin, 'data': data}, context_instance=RequestContext(request))

def partners(request):
    dpartners = Data.objects.get(id=11)
    formlogin = slogin(request)
    partner_list = PartnerModel.objects.all()
    return render_to_response('webapp/partners.html', {'dpartners': dpartners, 'formlogin': formlogin, 'partner_list': partner_list}, context_instance=RequestContext(request))

def partnersform(request):
	if request.method == "POST":
		form = PartnersForm(request.POST)
		if form.is_valid():
			model_instance = form.save(commit=False)
			model_instance.save()
			return redirect('partners')
	else:
			form = PartnersForm()
	return render(request, "webapp/forms.html", {'form': form})

def formsucces(request):
	return render(request, 'webapp/formsucces.html')

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

def register(request):
    if request.user.is_authenticated():
        return redirect('/')
    registration_form = RegistrationForm()
    formlogin=AuthenticationForm()
    if request.method == 'POST' and 'loginbtn' in request.POST:
        formlogin = AuthenticationForm(data=request.POST)
        if formlogin.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return redirect('/')
                else:
                    return redirect("/login")
            else:
                return redirect("/login")
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
	return render_to_response('webapp/edit/pand.html', {'pand': pand, 'fotos': fotos}, context_instance=RequestContext(request))
def login(request):
    if request.method == 'POST' and 'loginbtn' in request.POST:
        form = AuthenticationForm()
        formlogin = AuthenticationForm(data=request.POST)
        if formlogin.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return render_to_response('webapp/login.html', {'form': form, 'formlogin': formlogin}, context_instance=RequestContext(request))
    else:
        formlogin=AuthenticationForm()
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
        'formlogin': formlogin
	}, context_instance=RequestContext(request))

# def loginpopup(request):
# 	"""
#     Log in view
#     """
# 	if request.method == 'POST':
#       formlogin = AuthenticationForm(data=request.POST)
# 		if form.is_valid():
# 			user = authenticate(email=request.POST['email'], password=request.POST['password'])
# 			if user is not None:
# 				if user.is_active:
# 					django_login(request, user)
# 					return redirect('/')
# 	else:
# 		form = AuthenticationForm()
# 	return render_to_response('webapp/loginpopup.html', {
# 		'form': form,
# 	}, context_instance=RequestContext(request))

def sacha(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            return redirect('formsucces')
    else:
            form = SearchForm()
    return render(request, "webapp/forms.html", {'form': form})
