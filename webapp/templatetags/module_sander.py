from django import template
register = template.Library()
from webapp.models import *

@register.simple_tag
def get_obj_data(pk, attr):
    obj = getattr(Data.objects.get(pk=int(pk)), attr)
    return obj
