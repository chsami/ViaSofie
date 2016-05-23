from django.contrib import admin
from django.template import RequestContext
from django.conf.urls import patterns
from django.shortcuts import render_to_response
from .models import *
from django.contrib.admin import AdminSite

# Makelaar/Sofie
class MakelaarsPaneel(AdminSite):
    site_header = 'Sacha was hier'

admin_site = MakelaarsPaneel(name='makelaarspaneel')
admin_site.register(User)
admin_site.register(Pand)
admin_site.register(Handelstatus)
admin_site.register(Voortgang)
admin_site.register(Stad)
admin_site.register(Log)
admin_site.register(Tag)
admin_site.register(Foto)


# Admin/root
admin.site.register(User)
admin.site.register(Pand)
admin.site.register(Handelstatus)
admin.site.register(Voortgang)
admin.site.register(Stad)
admin.site.register(Log)
admin.site.register(Tag)
admin.site.register(Foto)
