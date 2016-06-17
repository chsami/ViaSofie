from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import render_to_string, get_template
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
from webapp.models import Tag as TagModel
from webapp.models import Stad as StadModel
from webapp.models import StatusBericht as StatusBerichtModel
from webapp.models import Handelstatus as HandelstatusModel
from django.utils.translation import ugettext as _
from webapp.forms import *
import hashlib
import random
from django.utils import timezone
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives, EmailMessage 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.loader import render_to_string

from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
from django.contrib.auth.forms import  PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import resolve_url

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
                    return False
            else:
                return False

    else:
        formlogin=AuthenticationForm()
    return formlogin

# def filtertags(request):
#     if request.method == 'POST' and 'searchbtn' in request.POST:
        # panden = PandModel.objects.filter()

def get_all_tags(request):
    all_tagpand_list = TagModel.objects.all()

    all_tags = []
    temp_tag = ""
    for tagpand in all_tagpand_list:
        for i in range(0,20):
            temp_tag = "%s (%s)" % (str(tagpand.tagnaam), str(i + 1))
            all_tags.append(temp_tag)
    return all_tags

# Create your views here.

def index(request):
    dpartners = Data.objects.get(id=11)

    formlogin = slogin(request)
    if formlogin == False:
        return redirect('/login')

    if request.method == "POST":
        searchform = SearchForm(request.POST)
        # if searchform.is_valid():
        handelstatus = request.POST['kopen']
            # if kopen == 'true':
            #     return redirect('/contact')
            # elif kopen == 'false':
            #     return redirect('/panden')
        plaats_postcode_renummer = request.POST['plaats_postcode_refnummer']

        pand_type = request.POST['pand_type']
            # aantal_badkamers = request.POST['aantal_badkamers']

        prijs_range = None
        if handelstatus == 'kopen':
            prijs_range = request.POST['prijsSliderKopen']
        else:
            prijs_range = request.POST['prijsSliderHuren']
            # aantal_slaapkamers = request.POST['aantal_slaapkamers']
            # aantal_verdiepen = request.POST['aantal_verdiepen']
        tags = request.POST['tagsSearch']

        filters ='handelstatus=' + handelstatus + '&plaats_postcode_refnummer=' + plaats_postcode_renummer + '&prijs_range=' + prijs_range + '&tags=' + pand_type + ',' + tags

        if filters.endswith(','):
            filters = filters[:-1]
            # lijst = [kopen, plaats_postcode, pand_type, aantal_badkamers, prijs_range, aantal_slaapkamers, prijs_range, aantal_slaapkamers, aantal_verdiepen, tags]
        return redirect('/panden/' + filters)


            # model_instance = smallsearchform.save(commit=False)
            # model_instance.save()

    else:
            searchform = SearchForm()

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
    return render_to_response('webapp/index.html', {'dpartners': dpartners, 'uitgelichte_panden': uitgelichte_panden, 'goede_doelen': goede_doelen,'searchform':searchform, 'formlogin':formlogin, 'partner_list': partner_list,},  context_instance=RequestContext(request))
# def index(request):
#     dpartners = Data.objects.get(id=11)
#
#     formlogin = slogin(request)
#     if formlogin == False:
#         return redirect('/login')
#
#     if request.method == "POST":
#         smallsearchform = SmallSearchForm(request.POST)
#         if smallsearchform.is_valid():
#             kopen = request.POST['kopen']
#             if kopen == 'true':
#                 return redirect('/contact')
#             elif kopen == 'false':
#                 return redirect('/panden')
#
#             # model_instance = smallsearchform.save(commit=False)
#             # model_instance.save()
#
#     else:
#             searchform =SearchForm()
#
#     panden = PandModel.objects.filter(uitgelicht=True)
#     panden_lijst = list(panden)
#     uitgelichte_panden = []
#     for i in range (0,3):
#         if len(panden_lijst) > 0:
#             uitgelichte_panden.append(panden_lijst.pop(random.randint(0, len(panden_lijst) -1)))
#     # GOEDE DOELEN
#     goede_doelen = GoedDoelModel.objects.all()
#     #PARTNERS
#     partner_list = PartnerModel.objects.all()
#     return render_to_response('webapp/index.html', {'dpartners': dpartners, 'uitgelichte_panden': uitgelichte_panden, 'goede_doelen': goede_doelen,'searchform':searchform, 'formlogin':formlogin, 'partner_list': partner_list,},  context_instance=RequestContext(request))

def panddetail(request, pand_referentienummer):
    formlogin = slogin(request)
    if formlogin == False:
        return redirect('/login')
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
    url = request.build_absolute_uri()

    all_tags = get_all_tags(request);

    return render_to_response('webapp/pand.html', {'pand': pand, 'fotos' : fotos, 'relatedPands' : relatedPands, 'tag_data': tag_data, 'all_tags': all_tags,'url': url , 'formlogin':formlogin}, context_instance=RequestContext(request))

def panden(request, filters=None):
    # filters ='handelstatus=' + handelstatus + '&plaats_postcode_refnummer=' + plaats_postcode_renummer + '&prijs_range=' + prijs_range + '&tags=' + pandtype + ',' + tags
    # REMOVE LINE ABOVE
    panden = PandModel.objects.all()
    if filters:
        panden = []
        result_queryset = PandModel.objects.all()
        filtersets = filters.split('&')
        for filterset in filtersets:
            if 'handelstatus' in filterset:
                # handelstatus_id = HandelstatusModel.objects.filter()
                result_queryset.filter(handelstatus=filterset.split('=')[1])

            elif 'plaats_postcode_refnummer' in filterset:
                if filterset.split('=')[1].isdigit():
                    postcode_id = StadModel.objects.get(postcode=filterset.split('=')[1]).id
                    result_queryset = result_queryset.filter(postcodeID=postcode_id)
                elif ilterset.split('=')[1].replace('-', '').isalpha():
                    postcode_id = StadModel.objects.get(stadsnaam=filterset.split('=')[1]).id
                    result_queryset = result_queryset.filter(postcodeID=postcode_id)
                else:
                    result_queryset = result_queryset.filter(referentienummer=filterset.split('=')[1])

            elif 'prijs_range' in filterset:
                result_queryset = result_queryset.filter(prijs__gte=int(filterset.split('=')[1].split(',')[0])).filter(prijs__lte=int(filterset.split('=')[1].split(',')[1]))

            # Check for tags and fill list with pand_id's
            tags_queryset = TagPandModel.objects.all()
            if 'tags' in filterset:
                tags = filterset.split('=')[1].split(',')
                for single_tag in tags:
                    tag_id = TagModel.objects.get(tagnaam=single_tag.split(':')[0]).id
                    tags_queryset = tags_queryset.filter(tag=tag_id)
                    tags_queryset = tags_queryset.filter(value__gte=int(single_tag.split(':')[1]))

        pand_ids = None
        for tag in tags_queryset:
            pand_ids.append(tag.pand.id)

        for pand in result_queryset:
            for pand_id in pand_ids:
                if result_queryset.filter(pk=pand_id):
                    panden.append(result_queryset.filter(pk=pand_id))

    data = Data.objects.get(id=13)
    # Login form
    formlogin = slogin(request)
    if formlogin == False:
        return redirect('/login')
    # SmallSearchForm
    if request.method == "POST":
        smallsearchform = SmallSearchForm(request.POST)
        if smallsearchform.is_valid():
            model_instance = smallsearchform.save(commit=False)
            model_instance.save()
            return redirect('formsucces')
    else:
            smallsearchform = SmallSearchForm()
    # SearchForm
    if request.method == "POST":
        searchform = SearchForm(request.POST)
        if searchform.is_valid():

            return redirect('/panden')
    else:
            searchform = SearchForm()

    all_tags = get_all_tags(request);

    # Context (endless pagination)
    context = {
        'panden': panden,
        'panden_item': 'webapp/panden_item.html',
        'formlogin': formlogin,
        'data': data,
        'searchform': searchform,
        'all_tags': all_tags,
    }
    template = 'webapp/panden.html'
    if request.is_ajax():
        template = 'webapp/panden_item.html'
    return render_to_response(template, context, context_instance=RequestContext(request))

# def panden(request, filters=None):
#     data = Data.objects.get(id=13)
#     # Login form
#     formlogin = slogin(request)
#     if formlogin == False:
#         return redirect('/login')
#     # SmallSearchForm
#     if request.method == "POST":
#         smallsearchform = SmallSearchForm(request.POST)
#         if smallsearchform.is_valid():
#             model_instance = smallsearchform.save(commit=False)
#             model_instance.save()
#             return redirect('formsucces')
#     else:
#             smallsearchform = SmallSearchForm()
#     # SearchForm
#     if request.method == "POST":
#         searchform = SearchForm(request.POST)
#         if searchform.is_valid():
#
#             return redirect('/panden')
#     else:
#             searchform = SearchForm()
#
#     all_tags = get_all_tags(request);
#
#     # Context (endless pagination)
#     context = {
#         'panden': PandModel.objects.all().values(),
#         'panden_item': 'webapp/panden_item.html',
#         'formlogin': formlogin,
#         'data': data,
#         'searchform': searchform,
#         'all_tags': all_tags,
#     }
#     template = 'webapp/panden.html'
#     if request.is_ajax():
#         template = 'webapp/panden_item.html'
#     return render_to_response(template, context, context_instance=RequestContext(request))

def referenties(request):
    data = Data.objects.get(id=9)
    formlogin = slogin(request)
    if formlogin == False:
        return redirect('/login')
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
    if formlogin == False:
        return redirect('/login')
    current_user = request.user

    # StatusBericht
    status_berichten = StatusBerichtModel.objects.filter(user=current_user)

    # Panden van de gebruiker
    panden = PandModel.objects.filter(user=current_user)

    if current_user.is_authenticated():
        # Do something for authenticated users.
        return render_to_response('webapp/account.html', {'current_user': current_user, 'status_berichten': status_berichten, 'panden': panden, 'formlogin': formlogin}, context_instance=RequestContext(request))
    else:
        # Do something for anonymous users.
        return render_to_response('webapp/account.html', {'current_user': current_user, 'status_berichten': status_berichten, 'panden': panden, 'formlogin': formlogin}, context_instance=RequestContext(request))


def about(request):
    dabout = Data.objects.get(id=10)
    formlogin = slogin(request)
    if formlogin == False:
        return redirect('/login')
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
            try:
                msg_html = render_to_string('webapp/emailcontact.html', {'message': message, 'name': name})
                send_mail(subject,"", sender, ['liekensjeff@gmail.com'], html_message=msg_html,)

            except BadHeaderError:
                return HttpResponse("invalid.")
        form = ContactForm()
    else:
        form = ContactForm()
        formlogin = AuthenticationForm()
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
    if formlogin == False:
        return redirect('/login')
    faq_list = FaqModel.objects.all()
    return render_to_response('webapp/advies.html', {'dadvies': dadvies, 'dfaq': dfaq, 'faq_list': faq_list, 'formlogin': formlogin}, context_instance=RequestContext(request))

def huren(request):
    formlogin = slogin(request)
    if formlogin == False:
        return redirect('/login')
    return render_to_response('webapp/huren.html', {'formlogin': formlogin}, context_instance=RequestContext(request))

def kopen(request):
    formlogin = slogin(request)
    if formlogin == False:
        return redirect('/login')
    return render_to_response('webapp/kopen.html', {'formlogin': formlogin}, context_instance=RequestContext(request))

def disclaimer(request):
    data = Data.objects.get(id=1)
    formlogin = slogin(request)
    if formlogin == False:
        return redirect('/login')
    return render_to_response('webapp/disclaimer.html', {'formlogin': formlogin, 'data': data}, context_instance=RequestContext(request))

def privacy(request):
    data = Data.objects.get(id=2)
    formlogin = slogin(request)
    if formlogin == False:
        return redirect('/login')
    return render_to_response('webapp/privacy.html', {'formlogin': formlogin, 'data': data}, context_instance=RequestContext(request))

def partners(request):
    dpartners = Data.objects.get(id=11)
    formlogin = slogin(request)
    if formlogin == False:
        return redirect('/login')
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
	return render(request, "webapp/ebook.html", {'form': form})

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
            datas['voornaam']=form.cleaned_data['voornaam']
            datas['naam']=form.cleaned_data['naam']
            #We will generate a random activation key
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            emailsalt = datas['email']
            if isinstance(emailsalt, unicode):
                emailsalt = emailsalt.encode('utf8')
            datas['activation_key']=hashlib.sha1(salt+emailsalt).hexdigest()

            datas['activation_email']=request.build_absolute_uri('/').strip("/") + '/activate/' + datas['activation_key']
            datas['email_path']="webapp/activation/ActivationEmail.html"
            datas['email_subject']="Welkom bij ViaSofie"

            ctx = {
                'voornaam': datas['voornaam'],
                'naam': datas['naam'],
                'activation_link': datas['activation_email']
            }

            message = get_template(datas['email_path']).render(Context(ctx))

            try:
                msg = EmailMessage(datas['email_subject'], message, 'noreply@viasofie.be', [datas['email']])
                msg.content_subtype = "html"
                msg.send()
            except BadHeaderError:
                return HttpResponse("invalid.")

            # form.sendEmail(datas) #Send validation email
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
                return redirect('/login')
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

#<--------customized django view---------->
@csrf_protect
def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   extra_context=None,
                   html_email_template_name=None,
                   extra_email_context=None):

    formlogin=AuthenticationForm()
    form = password_reset_form()

    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
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

    elif request.method == "POST":
        formlogin=AuthenticationForm()
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
                'extra_email_context': extra_email_context,
            }
            if is_admin_site:
                warnings.warn(
                    "The is_admin_site argument to "
                    "django.contrib.auth.views.password_reset() is deprecated "
                    "and will be removed in Django 1.10.",
                    RemovedInDjango110Warning, 3
                )
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('Password reset'),
        'formlogin': formlogin

    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)
