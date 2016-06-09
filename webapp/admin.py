from django.contrib import admin
from django.template import RequestContext
from django.conf.urls import patterns
from django.shortcuts import render_to_response
from .models import *
from django.contrib.admin import AdminSite

# Admin/root
admin.site.register(User)
admin.site.register(Pand)
admin.site.register(Handelstatus)
admin.site.register(Voortgang)
admin.site.register(Stad)
admin.site.register(Log)
admin.site.register(Tag)
admin.site.register(Foto)
admin.site.register(Faq)
admin.site.register(TagPand)
admin.site.register(StatusBericht)