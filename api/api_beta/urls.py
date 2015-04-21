from django.conf.urls import patterns, url, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = patterns('',
                        url(r'^login/', include('rest_framework.urls', namespace='rest_framework')),
                        url(r'^accounts/', include('djoser.urls')),
                        url(r'^profiles/$', views.PublicUserProfileList.as_view(), name='public-profiles'),
                        url(r'^profiles/(?P<pk>[0-9]+)/$', views.UserProfileDetail.as_view(), name='user-profile-detail'),
                        url(r'^kits/$', views.KitList.as_view(), name='kit-list'),
                        url(r'^kits/(?P<pk>[0-9]+)/$', views.KitDetail.as_view(), name='kit-detail'),
                        url(r'^samples/$', views.SampleDemoList.as_view()),
                        url(r'^samples/(?P<pk>[0-9]+)/$', views.SampleDemoDetail.as_view()),
                        url(r'^descriptions/$', views.KitDescriptionList.as_view()),
                        # url(r'^api/samples/endproducts/$', views.SampleList.as_view()),
                        # url(r'^api/samples/endproducts/(?P<pk>[0-9]+)/$', views.SampleDetail.as_view()),
                        url(r'^custom-kits/$', views.CustomKitList.as_view()),
                        url(r'^custom-kits/(?P<pk>[0-9]+)/$', views.CustomKitDetail.as_view()),
                        # purchase view requires csrf token.
                        #url(r'^api/custom-kits/purchase/$', csrf_exempt(views.CustomKitPaymentView.as_view())),
                        url(r'^custom-kits/purchase/$', views.CustomKitPaymentView.as_view()),
                       )

