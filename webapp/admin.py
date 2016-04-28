from django.contrib import admin
from .models import User, Pand, PandType, Handelstatus, Voortgang, Stad, Log, Tag, Foto

admin.site.register(User)
admin.site.register(Pand)
admin.site.register(PandType)
admin.site.register(Handelstatus)
admin.site.register(Voortgang)
admin.site.register(Stad)
admin.site.register(Log)
admin.site.register(Tag)
admin.site.register(Foto)