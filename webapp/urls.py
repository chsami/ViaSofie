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
    url(r'^sander/$', views.sander, name='sander'),
    url(r'^register/$', views.register, name='register'),

    # user auth urls
    url(r'^accounts/login/$',  'django_test.views.login'),
    url(r'^accounts/auth/$',  'django_test.views.auth_view'),
    url(r'^accounts/logout/$', 'django_test.views.logout'),
    url(r'^accounts/loggedin/$', 'django_test.views.loggedin'),
    url(r'^accounts/invalid/$', 'django_test.views.invalid_login'),

]
