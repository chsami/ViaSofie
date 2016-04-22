from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^advies/$', views.advies, name='advies'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^huren/$', views.huren, name='huren'),
    url(r'^kopen/$', views.kopen, name='kopen'),
    url(r'^partners/$', views.partners, name='partners'),
    url(r'^sander/$', views.sander, name='sander'),
    url(r'^register/$', views.register, name='register'),

    # user auth urls
    url(r'^login/$', views.login, name='login'),
    url(r'^auth/$',  views.auth_view, name='auth'),
    url(r'^logout/$', views.logout),
    url(r'^loggedin/$', views.loggedin),
    url(r'^invalid/$', views.invalid_login),

]
