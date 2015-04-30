from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings
import local_settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CustomDrumSamples.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('kitbuilder.urls')),
    url(r'^', include('api.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        # url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        #     'document_root': local_settings.MEDIA_ROOT,
        # }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': local_settings.STATIC_ROOT,
        }),
)
