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
    url(r'^sander/$', views.stad, name='sander'),
    url(r'^register/$', views.gebruiker, name='register'),
    url(r'^ebook/$', views.ebook, name='register'),
    url(r'^formsucces/$', views.formsucces, name='formsucces'),
]