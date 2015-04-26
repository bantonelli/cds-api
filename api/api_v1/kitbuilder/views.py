from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from api.permissions import IsKitOwner, IsUser
from serializers import *
from kitbuilder.kitbuilder_v1.models import Sale, Tag, Vendor, VendorKit, Sample, KitBuilderPurchase, KitBuilderTemplate
from userprofile.models import UserProfile
from djoser.utils import ActionViewMixin, SendEmailViewMixin
from djoser.views import OauthUserMixin



########### API VIEWS


#SOUND SAMPLE
class SamplePreviewList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    required_scopes = ['read']
    queryset = Sample.objects.all()
    serializer_class = SamplePreviewSerializer


class SamplePreviewDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    required_scopes = ['read']
    queryset = Sample.objects.all()
    serializer_class = SamplePreviewSerializer


#SAMPLE KIT
class VendorKitList(generics.ListAPIView):
    """
    List all Drum Kits
    """
    permission_classes = (permissions.IsAuthenticated, )
    required_scopes = ['read']
    queryset = VendorKit.objects.all()
    serializer_class = VendorKitSerializer


class VendorKitDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAdminUser, )
    queryset = VendorKit.objects.all()
    serializer_class = VendorKitSerializer


#-------------------------------------------------------------->
# KIT BUILDER PURCHASE
# class KitBuilderPurchaseList(generics.ListCreateAPIView):
#     permission_classes = (permissions.IsAdminUser, )
#     queryset = KitBuilderPurchase.objects.all()
#     serializer_class = KitBuilderPurchaseSerializer


class KitBuilderPurchaseDetail(generics.RetrieveDestroyAPIView):
    # Make Custom permission so that it checks if is authenticated and is user that purchased kit
    permission_classes = (permissions.IsAuthenticated, IsKitOwner, )
    required_scopes = ['read']
    queryset = KitBuilderPurchase.objects.all()
    serializer_class = KitBuilderPurchaseSerializer


class KitBuilderTemplateList(generics.ListCreateAPIView, OauthUserMixin):
    permission_classes = (permissions.IsAuthenticated, )
    required_scopes = ['read']
    queryset = KitBuilderTemplate.objects.all()
    serializer_class = KitBuilderTemplateSerializer

# Grabs the user
# Use the OAuth User mixin for this
# checks the user's list of KitBuilderTemplates
# If the KitBuilderTemplate that they have already exists return an error
# If not create it and return a success message.
    def create(self, request, *args, **kwargs):
        serializer = KitBuilderTemplateSerializer(data=request.data)
        user = self.get_current_user(request)
        if serializer.is_valid():
            template_name = request.data['name']
            if user is not None:
                users_templates = user.profile.kitbuilder_templates.all()
                if users_templates.filter(name=template_name).exists():
                    data = {"template_created": False, "data_error": "You already have a kitbuilder template with that name!"}
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.save(user=user.profile)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KitBuilderTemplateDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsKitOwner, )
    required_scopes = ['read']
    queryset = KitBuilderTemplate.objects.all()
    serializer_class = KitBuilderTemplateSerializer
