from django.conf.urls import url, include

from . import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    #url(r'^pand/$', views.pand, name='pand'),
    url(r'^pand/(?P<pand_referentienummer>[a-zA-Z0-9_]+)$', views.panddetail, name='panddetail'),
    url(r'^about/$', views.about, name='about'),
    url(r'^advies/$', views.advies, name='advies'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^huren/$', views.huren, name='huren'),
    url(r'^kopen/$', views.kopen, name='kopen'),
    url(r'^partners/$', views.partners, name='partners'),
    url(r'^panden/$', views.panden, name='panden'),
    url(r'^referenties/$', views.referenties, name='referenties'),
    url(r'^disclaimer/$', views.disclaimer, name='disclaimer'),
    url(r'^loginpopup/$', views.loginpopup, name='loginpopup'),

    #Auth
    url(r'^register/$', views.register, name='register'),
    url(r'^activate/(?P<key>.+)$', views.activation, name='activation'),
    url(r'^new-activation-link/(?P<user_id>\d+)/$', views.new_activation_link, name='new_activation_link'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^resetpassword/$',  'django.contrib.auth.views.password_reset',  {'template_name': 'webapp/password_reset/password_reset_form.html', 'post_reset_redirect' : 'passwordsent/'}, name='password_reset'),
    url(r'^resetpassword/passwordsent/',  'django.contrib.auth.views.password_reset_done', {'template_name': 'webapp/password_reset/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',  'django.contrib.auth.views.password_reset_confirm', {'template_name': 'webapp/password_reset/password_reset_confirm.html', 'post_reset_redirect' : '/reset/done/'}, name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'webapp/password_reset/password_reset_complete.html'}, name='password_reset_complete'),

    #Form urls
    url(r'^forms/$', views.forms, name='forms'),
    url(r'^stad/$', views.stad, name='stad'),
    url(r'^handelstatus/$', views.handelstatus, name='handelstatus'),
    url(r'^voortgang/$', views.voortgang, name='voortgang'),
    #url(r'^pand/$', views.pand, name='pand'),
    url(r'^tag/$', views.tag, name='tag'),
    url(r'^log/$', views.log, name='log'),
    url(r'^foto/$', views.foto, name='foto'),
    url(r'^formsucces/$', views.formsucces, name='formsucces'),

    #Ebook
    url(r'^ebook/form/$', views.ebooks, name='ebooks'),
    url(r'^ebook/lijst/$', views.ebook_lijst, name='ebook_lijst'),

    #taal
    url(r'^languageselector/$', views.languageselector, name='languageselector'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
