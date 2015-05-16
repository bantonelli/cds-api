__author__ = 'brandonantonelli'
from rest_framework import generics, permissions
from rest_framework.parsers import JSONParser, MultiPartParser
from provider.oauth2.models import AccessToken
from userprofile.models import UserProfile
from serializers import UserProfilePublicSerializer, UserProfilePrivateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


#-------------------------------------------------------------->
# (PUBLIC) USER PROFILE LIST - (used by site to show featured profiles)
class UserProfileList(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    required_scopes = ['read']
    queryset = UserProfile.objects.all()
    serializer_class = UserProfilePublicSerializer


#-------------------------------------------------------------->
# (PUBLIC/PRIVATE) USER PROFILE DETAIL - (private serializer used if current user owns the profile)
class UserProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    required_scopes = ['read']
    queryset = UserProfile.objects.all()
    serializer_class = UserProfilePublicSerializer
    parser_classes = (JSONParser, MultiPartParser)

    def get_serializer_class(self, *args, **kwargs):
        user_id = self.kwargs.get(self.lookup_field)
        lookup_user = User.objects.get(pk=user_id)
        current_user = None
        try:
            auth_header = self.request.META['Authorization']
            index = auth_header.find('Bearer') + 7
            token_string = auth_header[index:]
            token = AccessToken.objects.get_token(token=token_string)
            current_user = token.user
        except:
            current_user = self.request.user
        if lookup_user == current_user:
            return UserProfilePrivateSerializer
        else:
            return UserProfilePublicSerializer


