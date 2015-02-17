from rest_framework import generics, permissions
from permissions import IsKitOwner, IsUser
from serializers import *
from provider.oauth2.models import AccessToken
from kitbuilder.models import Sale, Tag, KitDescription, Kit, Sample, CustomKit
from userprofile.models import UserProfile


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


#USER PROFILES
class PublicUserProfileList(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    required_scopes = ['read']
    queryset = UserProfile.objects.all()
    serializer_class = UserProfilePublicSerializer


class PublicUserProfileDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    required_scopes = ['read']
    queryset = UserProfile.objects.all()
    serializer_class = UserProfilePublicSerializer

class UserProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsUser,)
    required_scopes = ['read']
    serializer_class = UserProfilePrivateSerializer

    def get_object(self, *args, **kwargs):
        if self.request.user:
            return self.request.user.profile
        elif self.request.META['Authorization']:
            auth_header = self.request.META['Authorization']
            index = auth_header.find('Bearer') + 7
            token_string = auth_header[index:]
            token = AccessToken.objects.get_token(token=token_string)
            user = token.user
            return user.profile