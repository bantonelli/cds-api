from django.conf.urls import patterns, url, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns

from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
    url(r'^api/', include('api.beta.urls', namespace='beta')),
    url(r'^api/v1/', include('api.v1.urls', namespace='v1')),
)

urlpatterns = format_suffix_patterns(urlpatterns)
