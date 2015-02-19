from django.conf.urls import patterns, url, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = patterns('',
                        url(r'^api-login/', include('rest_framework.urls', namespace='rest_framework')), # User accessible
                        url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
                        url(r'^api/accounts/', include('djoser.urls')),
                        #url(r'^api/accounts/profile/$', views.UserProfileDetail.as_view()),
                        #url(r'^api/profiles/me/$', views.UserProfileDetail.as_view()),
                        url(r'^api/profiles/$', views.PublicUserProfileList.as_view(), name='public-profiles'),
                        url(r'^api/profiles/(?P<pk>[0-9]+)/$', views.UserProfileDetail.as_view(), name='user-profile-detail'),
                        url(r'^api/kits/$', views.KitList.as_view(), name='kit-list'), # User accessible
                        url(r'^api/kits/(?P<pk>[0-9]+)/$', views.KitDetail.as_view(), name='kit-detail'),
                        url(r'^api/samples/$', views.SampleDemoList.as_view()), # User accessible
                        url(r'^api/samples/(?P<pk>[0-9]+)/$', views.SampleDemoDetail.as_view()), # User accessible
                        url(r'^api/descriptions/$', views.KitDescriptionList.as_view()), # User accessible
                        # url(r'^api/samples/endproducts/$', views.SampleList.as_view()),
                        # url(r'^api/samples/endproducts/(?P<pk>[0-9]+)/$', views.SampleDetail.as_view()),
                        url(r'^api/custom-kits/$', views.CustomKitList.as_view()),
                        url(r'^api/custom-kits/(?P<pk>[0-9]+)/$', views.CustomKitDetail.as_view()), # Only User accessible
                        url(r'^api/custom-kits/purchase/$', csrf_exempt(views.CustomKitPaymentView.as_view())),
                       )

urlpatterns = format_suffix_patterns(urlpatterns)
