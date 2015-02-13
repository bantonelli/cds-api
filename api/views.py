from django.shortcuts import render_to_response
from django.views.generic.base import View
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse
import urllib
import urllib2

from serializers import *
from rest_framework import generics, permissions
from permissions import IsKitOwner, IsUser
#from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
########### API VIEWS


#SOUND SAMPLE
class SampleDemoList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    required_scopes = ['read']
    queryset = Sample.objects.all()
    serializer_class = SampleDemoSerializer


class SampleDemoDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    required_scopes = ['read']
    queryset = Sample.objects.all()
    serializer_class = SampleDemoSerializer


#SAMPLE KIT
class KitList(generics.ListAPIView):
    """
    List all Drum Kits
    """
    permission_classes = (permissions.IsAuthenticated, )
    required_scopes = ['read']
    queryset = Kit.objects.all()
    serializer_class = KitSerializer


class KitDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAdminUser, )
    queryset = Kit.objects.all()
    serializer_class = KitSerializer


#KIT DESCRIPTIONS (USE FOR QUICK TESTING)
class KitDescriptionList(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser, )
    required_scopes = ['read']
    queryset = KitDescription.objects.all()
    serializer_class = KitDescriptionSerializer


#CUSTOM KIT
class CustomKitList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAdminUser, )
    queryset = CustomKit.objects.all()
    serializer_class = CustomKitSerializer


class CustomKitDetail(generics.RetrieveDestroyAPIView):
    # Make Custom permission so that it checks if is authenticated and is user that created kit
    permission_classes = (permissions.IsAuthenticated, IsKitOwner, )
    required_scopes = ['read']
    queryset = CustomKit.objects.all()
    serializer_class = CustomKitPurchasedSerializer


#USER
class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser, )
    required_scopes = ['read']
    queryset = User.objects.all()
    serializer_class = UserSerializer



# curl -X POST -d "client_id=21bc3b3e5b430572e41a&grant_type=password&username=brandonantonelli&password=123456" http://127.0.0.1:8000/oauth2/access_token/