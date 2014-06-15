from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'TransitSystem.views.home', name='home'),
    # url(r'^untitled/', include('untitled.foo.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^findbus/$','TransitSystem.views.findbus',name='findbus'),

    url(r'^searchbus/$','TransitSystem.views.searchbus',name='searchbus'),

    url(r'^schedule/$','TransitSystem.views.schedule',name='schedule'),
    url(r'^locate/$','TransitSystem.views.locate',name='locate'),
    url(r'^predictions/$','TransitSystem.views.predict',name='predict'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
