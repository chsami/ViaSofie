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
from webapp.models import PandDetail as PandDetailModel
from webapp.models import PandEPC as PandEPCModel
from webapp.models import PandDocument as PandDocumentModel
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
import collections

from geopy.geocoders import Nominatim

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

def ssearchform(request):
    if request.method == "POST" and "searchbtngo" in request.POST:
        searchform = SearchForm(request.POST)
        handelstatus = request.POST['kopen']
        plaats_postcode_renummer = request.POST['plaats_postcode_refnummer']
        if plaats_postcode_renummer == '':
            plaats_postcode_renummer = 'None'

        filters ='handelstatus=' + handelstatus + '&plaats_postcode_refnummer=' + plaats_postcode_renummer

        return '/panden/' + filters


            # model_instance = smallsearchform.save(commit=False)
            # model_instance.save()
    else:
        searchform = SearchForm()
    return searchform

# Create your views here.

def index(request):
    dpartners = Data.objects.get(id=11)

    formlogin = slogin(request)
    if formlogin == False:
        return redirect('/login')

    searchform = ssearchform(request)
    if isinstance(searchform, basestring):
        return redirect(searchform)
    panden = PandModel.objects.filter(uitgelicht=True)
    panden = panden.filter(voortgang=1)



    panden_lijst = list(panden)
    uitgelichte_panden = []
    for i in range (0,3):
        if len(panden_lijst) > 0:
            uitgelichte_panden.append(panden_lijst.pop(random.randint(0, len(panden_lijst) -1)))

    # Get photos + thumbnail picture (if no picture was selected to be a tumbnail, take the first out of all pictures)
    thumbnails = []
    for pand in uitgelichte_panden:
        fotos = FotoModel.objects.filter(pand_id=pand.id)
        try:
            thumbnail = fotos.filter(thumbnail=true)[:1]
        except Exception as ex:
            thumbnail = fotos[0]

        thumbnails.append(thumbnail)


    # GOEDE DOELEN
    goede_doelen = GoedDoelModel.objects.all()
    #PARTNERS
    partner_list = PartnerModel.objects.all()

    return render_to_response('webapp/index.html', {'dpartners': dpartners, 'uitgelichte_panden': uitgelichte_panden, 'thumbnails': thumbnails, 'goede_doelen': goede_doelen,'searchform':searchform, 'formlogin':formlogin, 'partner_list': partner_list,},  context_instance=RequestContext(request))


def panddetail(request, pand_referentienummer):
    formlogin = slogin(request)
    if formlogin == False:
        return redirect('/login')
    searchform = ssearchform(request)
    if isinstance(searchform, basestring):
        return redirect(searchform)
    pand = PandModel.objects.get(referentienummer=pand_referentienummer)
    #voeg extra gegevens toe
    relatedPands= PandModel.objects.filter(postcodeID=pand.postcodeID)
    relatedPands= relatedPands.filter(handelstatus=pand.handelstatus)
    relatedPands = relatedPands.filter(voortgang=1)

    # GET URL
    url = request.build_absolute_uri()

    # Get photos + thumbnail picture (if no picture was selected to be a tumbnail, take the first out of all pictures)
    fotos = FotoModel.objects.filter(pand_id=pand.id)
    try:
        thumbnail = fotos.filter(thumbnail=true)[:1]
    except Exception as ex:
        thumbnail = fotos[0]

    max_picture_count = list(range(6))


    # Get thumbnail pictures for related pands (if no picture was selected to be a tumbnail, take the first out of all pictures)
    thumbnails_related = []
    for related_pand in relatedPands:
        fotos = FotoModel.objects.filter(pand_id=related_pand.id)
        try:
            thumbnail = fotos.filter(thumbnail=true)[:1]
        except Exception as ex:
            thumbnail = fotos[0]

        thumbnails_related.append(thumbnail)


    fotos = FotoModel.objects.filter(pand_id=pand.id)
    try:
        thumbnail = fotos.filter(thumbnail=true)[:1]
    except Exception as ex:
        thumbnail = fotos[0]



    # Get details
    pand_details = PandDetailModel.objects.filter(pand_id = pand.id)

    # Get PandEPC
    pand_epc = PandEPCModel.objects.filter(pand_id = pand.id)

    # Get PandDocuments
    pand_documenten = PandDocumentModel.objects.filter(pand_id = pand.id)


    # Get lat long from adress
    geo_adress_string = str(pand.huisnr) + " " + str(pand.straatnaam) + " " + str(pand.postcodeID.stadsnaam) + " Belgie"
    geolocator = Nominatim()
    location = geolocator.geocode(geo_adress_string)

    lat = str(location.latitude).replace(',', '.')
    lng = str(location.longitude).replace(',', '.')

    return render_to_response('webapp/pand.html', {'pand': pand, 'pand_details': pand_details, 'pand_epc': pand_epc, 'pand_documenten': pand_documenten, 'max_picture_count': max_picture_count, 'fotos' : fotos, 'thumbnail': thumbnail, 'thumbnails_related': thumbnails_related, 'relatedPands' : relatedPands,'url': url , 'formlogin':formlogin, 'searchform': searchform, 'lat': lat, 'lng': lng}, context_instance=RequestContext(request))

def panden(request, filters=None):
    # filters ='handelstatus=' + handelstatus + '&plaats_postcode_refnummer=' + plaats_postcode_renummer
    # e.g. handelstatus%3D2&plaats_postcode_refnummer%3D01b28841418a4226b62e80eff5712b27/
    # REMOVE LINE ABOVE

    panden = PandModel.objects.all()
    if filters:
        panden = []
        result_queryset = PandModel.objects.all()
        result_queryset = result_queryset.filter(voortgang=1)
        if filters == "handelstatus=1":
            print "handelstatus=1"
            result_queryset = result_queryset.filter(handelstatus=1)
            for result in result_queryset:
                panden.append(result)
        elif filters == "handelstatus=2":
            print "handelstatus=2"
            result_queryset = result_queryset.filter(handelstatus=2)
            for result in result_queryset:
                panden.append(result)
        else:
            filtersets = filters.split('&')
            for filterset in filtersets:
                if 'handelstatus' in filterset:
                    result_queryset = result_queryset.filter(handelstatus=filterset.split('=')[1])
                    print(result_queryset)

                elif 'plaats_postcode_refnummer' in filterset:
                    if 'plaats_postcode_refnummer=None' not in filterset:
                        value_pl_pos_ref = filterset.split('=')[1]
                        #Postcode, indien cijfers
                        if value_pl_pos_ref.isdigit():
                            try:
                                #je hebt 1 stad in stadmodel zitten nu/ update meerdere steden
                                stadmodels = StadModel.objects.filter(postcode=value_pl_pos_ref)
                                #je filtert de result_queryset op de postcode
                                # result_queryset_temp = result_queryset
                                liststeden = []
                                for stadmodel in stadmodels:
                                    liststeden.append(stadmodel.id)

                                queryset = result_queryset.filter(postcodeID__in=liststeden)

                            except Exception as ex:
                                result_queryset = result_queryset[:0]

                        #Plaats, indien letters
                        elif value_pl_pos_ref.replace('-', '').isalpha() and value_pl_pos_ref.replace('-', '') != "":
                            #je hebt 1 stad in stadmodel zitten
                            try:
                                stadmodel = StadModel.objects.get(stadsnaam=value_pl_pos_ref)
                                result_queryset = result_queryset.filter(postcodeID=stadmodel.id)
                            except Exception as ex:
                                result_queryset = result_queryset[:0]
                        #referentienummer
                        elif value_pl_pos_ref.replace('-', '') != "":
                            #er kan maar 1 pand overeenkomstig zijn met ref nummer dus zoek maar 1 pand
                            #er moet nog ge-exit worden als het een ref nummer is
                            try:
                                result_queryset = result_queryset.filter(referentienummer=value_pl_pos_ref)
                            except Exception as ex:
                                pass

            try:
                for result in result_queryset:
                    panden.append(result)
            except TypeError as typeError:
                panden.append(result_queryset)


    data = Data.objects.get(id=13)
    # Login form
    formlogin = slogin(request)
    if formlogin == False:
        return redirect('/login')
    # Search form
    searchform = ssearchform(request)
    if isinstance(searchform, basestring):
        return redirect(searchform)
    else:
            searchform = SearchForm()

    # Get photos + thumbnail picture (if no picture was selected to be a tumbnail, take the first out of all pictures)
    thumbnails = []
    for pand in panden:
        fotos = FotoModel.objects.filter(pand_id=pand.id)
        try:
            thumbnail = fotos.filter(thumbnail=true)[:1]
        except Exception as ex:
            thumbnail = fotos[0]

        thumbnails.append(thumbnail)

    # Context (endless pagination)
    context = {
        'panden': panden,
        'thumbnails': thumbnails,
        'panden_item': 'webapp/panden_item.html',
        'formlogin': formlogin,
        'data': data,
        'searchform': searchform,
    }
    template = 'webapp/panden.html'
    if request.is_ajax():
        template = 'webapp/panden_item.html'
    return render_to_response(template, context, context_instance=RequestContext(request))

def referenties(request):
    data = Data.objects.get(id=9)
    formlogin = slogin(request)
    if formlogin == False:
        return redirect('/login')

    #filter panden op verkocht status
    panden = PandModel.objects.all()
    panden = panden.exclude(voortgang=1)
    #searchform
    searchform = ssearchform(request)
    if isinstance(searchform, basestring):
        return redirect(searchform)

    thumbnails = []
    for pand in panden:
        fotos = FotoModel.objects.filter(pand_id=pand.id)
        try:
            thumbnail = fotos.filter(thumbnail=true)[:1]
        except Exception as ex:
            thumbnail = fotos[0]

        thumbnails.append(thumbnail)

    context = {
        # 'panden' = PandModel.objects.get(handelstatus='Verkocht',handelstatus='Verhuurd')
        'searchform': searchform,
        'panden': panden,
        'thumbnails': thumbnails,
        'formlogin': formlogin,
        'data': data,
    }

    return render_to_response('webapp/referenties.html', context, context_instance=RequestContext(request))

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
    #searchform
    searchform = ssearchform(request)
    if isinstance(searchform, basestring):
        return redirect(searchform)
    formlogin = slogin(request)
    if formlogin == False:
        return redirect('/login')
    dadvies = Data.objects.get(id=8)
    dfaq = Data.objects.get(id=7)
    faq_list = FaqModel.objects.all()

    return render_to_response('webapp/advies.html', {'dadvies': dadvies, 'dfaq': dfaq, 'faq_list': faq_list, 'formlogin': formlogin, 'searchform': searchform,}, context_instance=RequestContext(request))

def vastgoedmakelaar(request):
    formlogin = slogin(request)
    if formlogin == False:
        return redirect('/login')
    return render_to_response('webapp/vastgoedmakelaar.html', {'formlogin': formlogin}, context_instance=RequestContext(request))

def samenwerken(request):
    formlogin = slogin(request)
    if formlogin == False:
        return redirect('/login')
    return render_to_response('webapp/samenwerken.html', {'formlogin': formlogin}, context_instance=RequestContext(request))

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
	return render(request, "webapp/partnersform.html", {'form': form})

def formsucces(request):
	return render(request, 'webapp/formsucces.html')

def ebooks(request):
	if request.method == "POST":
		form = Ebookform(request.POST)
		if form.is_valid():
			model_instance = form.save(commit=False)
			model_instance.save()
			return redirect('index')
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

def new_pand(request):
	return render_to_response('webapp/new_pand.html', context_instance=RequestContext(request))

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
