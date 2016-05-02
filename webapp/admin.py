from django.contrib import admin
from django.template import RequestContext
from django.conf.urls import patterns
from django.shortcuts import render_to_response
from .models import User, Pand, PandType, Handelstatus, Voortgang, Stad, Log, Tag, Foto

# class FotoAdmin(admin.ModelAdmin):
#     review_template = 'admin/foto.html'
#
#     def get_urls(self):
#         urls = super(FotoAdmin, self).get_urls()
#         my_urls = patterns('',
#             (r'\d+/foto/$', self.admin_site.admin_view(self.review)),
#         )
#         return my_urls + urls
#
#     def review(self, request, id):
#         foto = Foto.objects.get(pk=id)
#
#         return render_to_response(self.review_template, {
#             'title': 'Test',
#             'foto': foto,
#             'opts': self.model._meta,
#             'root_path': self.admin_site.root_path,
#         }, context_instance=RequestContext(request))

#admin.site.register(Foto, FotoAdmin)

# from functools import update_wrapper
# from django.contrib import admin
# from django.contrib.admin import ModelAdmin
# from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
# from django.core.exceptions import PermissionDenied
# from django.shortcuts import render
#
# from myapp.models import Widget
# from myapp.forms import ManageWidgetForm
#
#
# class WidgetAdmin(ModelAdmin):
#     change_form_template = 'myapp/change_form.html'
#     manage_view_template = 'myapp/manage_view.html'
#
#     def get_urls(self):
#         from django.conf.urls import patterns, url
#
#         def wrap(view):
#             def wrapper(*args, **kwargs):
#                 return self.admin_site.admin_view(view)(*args, **kwargs)
#             return update_wrapper(wrapper, view)
#
#         info = self.model._meta.app_label, self.model._meta.model_name
#
#         urls = patterns('',
#             url(r'^(.+)/manage/$',
#                 wrap(self.manage_view),
#                 name='%s_%s_manage' % info),
#         )
#
#         super_urls = super(WidgetAdmin, self).get_urls()
#
#         return urls + super_urls
#
#     def manage_view(self, request, id, form_url='', extra_context=None):
#         opts = Widget._meta
#         form = ManageWidgetForm()
#         obj = Widget.objects.get(pk=id)
#
#         if not self.has_change_permission(request, obj):
#             raise PermissionDenied
#
#         # do cool management stuff here
#
#         preserved_filters = self.get_preserved_filters(request)
#         form_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, form_url)
#
#         context = {
#             'title': 'Manage %s' % obj,
#             'has_change_permission': self.has_change_permission(request, obj),
#             'form_url': form_url,
#             'opts': opts,
#             'errors': form.errors,
#             'app_label': opts.app_label,
#             'original': obj,
#         }
#         context.update(extra_context or {})
#
#         return render(request, self.manage_view_template, context)
# admin.site.register(Widget, WidgetAdmin)
#
# @admin.register(Author, Reader, Editor, site=custom_admin_site)
# class FotoAdmin(admin.ModelAdmin):
#     pass

admin.site.register(User)
admin.site.register(Pand)
admin.site.register(PandType)
admin.site.register(Handelstatus)
admin.site.register(Voortgang)
admin.site.register(Stad)
admin.site.register(Log)
admin.site.register(Tag)
admin.site.register(Foto)
