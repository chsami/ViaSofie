from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'viasofie.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	#url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)), # admin site
    url(r'^', include('webapp.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# admin_site.index_template = 'admin/index.html'
