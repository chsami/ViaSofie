from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^advies/$', views.advies, name='advies'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^huren/$', views.huren, name='huren'),
    url(r'^kopen/$', views.kopen, name='kopen'),
    url(r'^login/$', views.login, name='login'),
    url(r'^partners/$', views.partners, name='partners'),
    
    #Form urls
    url(r'^stad/$', views.stad, name='stad'),
    url(r'^pandtype/$', views.pandtype, name='pandtype'),
    url(r'^handelstatus/$', views.handelstatus, name='handelstatus'),
    url(r'^voortgang/$', views.voortgang, name='voortgang'),
    url(r'^pand/$', views.pand, name='pand'),
    url(r'^tag/$', views.tag, name='tag'),
    url(r'^log/$', views.log, name='log'),
    url(r'^foto/$', views.foto, name='foto'),
    url(r'^formsucces/$', views.formsucces, name='formsucces'),
]