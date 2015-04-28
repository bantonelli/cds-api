from django.conf.urls import patterns, url, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns
from .kitbuilder.views import *
from .userprofile.views import *
import views

urlpatterns = patterns('',
                        url(r'^login/', include('rest_framework.urls', namespace='rest_framework')),
                        url(r'^accounts/', include('djoser.urls')),
                        url(r'^profiles/$', UserProfileList.as_view(), name='user-profiles'),
                        url(r'^profiles/(?P<pk>[0-9]+)/$', UserProfileDetail.as_view(), name='user-profile-detail'),
                        url(r'^kitbuilder/templates/$', KitBuilderTemplateList.as_view(), name='kitbuilder-template-list'),
                        url(r'^kitbuilder/templates/(?P<pk>[0-9]+)/$', KitBuilderTemplateDetail.as_view(), name='kitbuilder-template-detail'),
                        url(r'^kitbuilder/vendors/$', VendorList.as_view(), name='vendor-list'),
                        url(r'^kitbuilder/vendor-kits/$', VendorKitList.as_view(), name='vendor-kit-list'),
                        url(r'^kitbuilder/vendor-kits/(?P<pk>[0-9]+)/$', VendorKitDetail.as_view(), name='vendor-kit-detail'),
                        url(r'^kitbuilder/samples/$', SamplePreviewList.as_view()),
                        url(r'^kitbuilder/samples/(?P<pk>[0-9]+)/$', SamplePreviewDetail.as_view()),
                        # # url(r'^api/samples/endproducts/$', views.SampleList.as_view()),
                        # # url(r'^api/samples/endproducts/(?P<pk>[0-9]+)/$', views.SampleDetail.as_view()),
                        url(r'^kitbuilder/purchases/(?P<pk>[0-9]+)/$', KitBuilderPurchaseDetail.as_view()),
                        # purchase view requires csrf token.
                        url(r'^kitbuilder/purchase/$', views.KitBuilderPaymentView.as_view()),
                       )

