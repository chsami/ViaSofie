from django.conf.urls import url, include
from django.contrib.auth import views as viewsauth

from . import views

urlpatterns = [
    url(r'^rosetta/', include('rosetta.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^pand/(?P<pand_referentienummer>[a-zA-Z0-9_]+)/$', views.panddetail, name='panddetail'),
    url(r'^new/pand/$', views.new_pand, name='new_pand'),
    url(r'^about/$', views.about, name='about'),
    url(r'^advies/$', views.advies, name='advies'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^huren/$', views.huren, name='huren'),
    url(r'^kopen/$', views.kopen, name='kopen'),
    url(r'^partners/$', views.partners, name='partners'),
    url(r'^partnersform/$', views.partnersform, name='partnersorm'),
    url(r'^panden/$', views.panden, name='panden'),
    url(r'^panden/(?P<filters>[\W\w]+)/$', views.panden, name='panden'),
    url(r'^referenties/$', views.referenties, name='referenties'),
    url(r'^disclaimer/$', views.disclaimer, name='disclaimer'),
    url(r'^privacy/$', views.privacy, name='privacy'),
    url(r'^account/$', views.account, name='account'),
    # url(r'^loginpopup/$', views.loginpopup, name='loginpopup'),


    #Auth
    url(r'^register/$', views.register, name='register'),
    url(r'^activate/(?P<key>.+)$', views.activation, name='activation'),
    url(r'^new-activation-link/(?P<user_id>\d+)/$', views.new_activation_link, name='new_activation_link'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^resetpassword/$',  views.password_reset,  {'template_name': 'webapp/password_reset/password_reset_form.html', 'post_reset_redirect' : 'passwordsent/'}, name='password_reset'),
    # url(r'^resetpassword/$',  viewsauth.password_reset,  {'template_name': 'webapp/password_reset/password_reset_form.html', 'post_reset_redirect' : 'passwordsent/'}, name='password_reset'),
    url(r'^resetpassword/$',  views.password_reset,  {'template_name': 'webapp/password_reset/password_reset_form.html', 'post_reset_redirect' : 'passwordsent/'}, name='password_reset'),
    url(r'^resetpassword/passwordsent/',  viewsauth.password_reset_done, {'template_name': 'webapp/password_reset/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',  viewsauth.password_reset_confirm, {'template_name': 'webapp/password_reset/password_reset_confirm.html', 'post_reset_redirect' : '/reset/done/'}, name='password_reset_confirm'),
    url(r'^reset/done/$', viewsauth.password_reset_complete, {'template_name': 'webapp/password_reset/password_reset_complete.html'}, name='password_reset_complete'),

    #Form urls
    url(r'^handelstatus/$', views.handelstatus, name='handelstatus'),
    url(r'^voortgang/$', views.voortgang, name='voortgang'),
    url(r'^tag/$', views.tag, name='tag'),
    url(r'^foto/$', views.foto, name='foto'),
    url(r'^formsucces/$', views.formsucces, name='formsucces'),

    #Ebook
    url(r'^ebook/$', views.ebooks, name='ebooks'),
    url(r'^ebook/lijst/$', views.ebook_lijst, name='ebook_lijst'),

    #taal
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
