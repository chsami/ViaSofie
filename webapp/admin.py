from django.contrib import admin
from django.template import RequestContext
from django.conf.urls import patterns
from django.shortcuts import render_to_response
from .models import *
from django.contrib.admin import AdminSite




admin.site.register(Foto)

class DocumentInlineAdmin(admin.TabularInline):
    verbose_name = "Pand Document"
    verbose_name_plural = "Pand Documents"
    model = PandPandDocument

class EPCInlineAdmin(admin.TabularInline):
    verbose_name = "Pand EPC"
    verbose_name_plural = "Pand EPCs"
    model = PandPandEPC

class DetailInlineAdmin(admin.TabularInline):
    verbose_name = "Pand Detail"
    verbose_name_plural = "Pand Details"
    model = PandPandDetail

class PandDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'naam')  


class PandAdmin(admin.ModelAdmin):
    list_display = ('referentienummer', 'straatnaam', 'plaats', 'user')
    inlines = [DetailInlineAdmin, EPCInlineAdmin, DocumentInlineAdmin]
    DetailInlineAdmin.can_delete = True

class Foto(admin.ModelAdmin):
    class Media:
        js = ('webapp/scripts/jquery.min.js', 'inlines.js',)



# Admin/root
admin.site.register(User)
admin.site.register(Pand, PandAdmin)
admin.site.register(PandDetail)
admin.site.register(PandEPC)
admin.site.register(PandDocument, PandDocumentAdmin)
admin.site.register(Handelstatus)
admin.site.register(Voortgang)
admin.site.register(Stad)
# admin.site.register(Log)

admin.site.register(Faq)
admin.site.register(StatusBericht)
# admin.site.register(Ebook)
admin.site.register(GoedDoel)
# admin.site.register(Data)
admin.site.register(BlijfOpDeHoogteUser)

