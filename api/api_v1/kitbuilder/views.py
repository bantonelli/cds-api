from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from api.permissions import IsTemplateOwner, IsKitOwner, IsUserProfileOwner
from serializers import *
from kitbuilder.kitbuilder_v1.models import Sale, Tag, Vendor, VendorKit, Sample, KitBuilderPurchase, KitBuilderTemplate
from userprofile.models import UserProfile
from djoser.utils import RetrieveActionViewMixin, ActionViewMixin, SendEmailViewMixin
from djoser.views import OauthUserMixin


########### API VIEWS
#-------------------------------------------------------------->
# TAG VIEWS
class TagList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    required_scopes = ['read']
    # queryset = Tag.objects.all()
    serializer_class = TagSerializer
    parser_classes = (JSONParser, MultiPartParser,)

    def patch(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        model = self.serializer_class.Meta.model
        if self.request.method == 'PATCH':
            request_items = self.request.data.get('request_items')
            if request_items is not None:
                return model.objects.filter(id__in=request_items)
            else:
                return model.objects.all()
        else:
            return model.objects.all()


#-------------------------------------------------------------->
# SAMPLE VIEWS
class SamplePreviewList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    required_scopes = ['read']
    # queryset = Sample.objects.all()
    serializer_class = SamplePreviewSerializer
    parser_classes = (JSONParser, MultiPartParser,)

    def patch(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        model = self.serializer_class.Meta.model
        if self.request.method == 'PATCH':
            request_items = self.request.data.get('request_items')
            if request_items is not None:
                return model.objects.filter(id__in=request_items)
            else:
                return model.objects.all()
        else:
            return model.objects.all()


class SamplePreviewDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    required_scopes = ['read']
    queryset = Sample.objects.all()
    serializer_class = SamplePreviewSerializer


#-------------------------------------------------------------->
# VENDOR VIEWS
class VendorList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    required_scopes = ['read']
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    parser_classes = (JSONParser, MultiPartParser,)

    def patch(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        model = self.serializer_class.Meta.model
        if self.request.method == 'PATCH':
            request_items = self.request.data.get('request_items')
            if request_items is not None:
                return model.objects.filter(id__in=request_items)
            else:
                return model.objects.all()
        else:
            return model.objects.all()


#-------------------------------------------------------------->
# VENDOR KIT VIEWS
class VendorKitList(generics.ListAPIView):
    """
    List all Drum Kits
    """
    permission_classes = (permissions.IsAuthenticated, )
    required_scopes = ['read']
    queryset = VendorKit.objects.all()
    serializer_class = VendorKitSerializer
    parser_classes = (JSONParser, MultiPartParser,)

    def patch(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        model = self.serializer_class.Meta.model
        if self.request.method == 'PATCH':
            request_items = self.request.data.get('request_items')
            if request_items is not None:
                return model.objects.filter(id__in=request_items)
            else:
                return model.objects.all()
        else:
            return model.objects.all()


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


#-------------------------------------------------------------->
# KIT BUILDER TEMPLATE VIEWS
class KitBuilderTemplateList(generics.ListCreateAPIView, OauthUserMixin):
    permission_classes = (permissions.IsAuthenticated, )
    required_scopes = ['read']
    # queryset = KitBuilderTemplate.objects.filter(public=True)
    serializer_class = KitBuilderTemplateSerializer
    parser_classes = (JSONParser, MultiPartParser,)
# Grabs the user
# Use the OAuth User mixin for this
# checks the user's list of KitBuilderTemplates
# If the KitBuilderTemplate that they have already exists return an error
# If not create it and return a success message.

    def patch(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        model = self.serializer_class.Meta.model
        if self.request.method == 'PATCH':
            request_items = self.request.data.get('request_items')
            if request_items is not None:
                return model.objects.filter(id__in=request_items, public=True)
            else:
                return model.objects.filter(public=True)
        else:
            return model.objects.filter(public=True)

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
    permission_classes = (permissions.IsAuthenticated, IsTemplateOwner, )
    serializer_class = KitBuilderTemplateSerializer
    queryset = KitBuilderTemplate.objects.all()
    # required_scopes = ['read']
    parser_classes = (JSONParser, MultiPartParser,)

    # This updates the KitBuilder Template
    # If you send a put request you need to include all of the fields
    # If you send a patch request you can do a partial update to the model
    # Also has Object level permission using the IsTemplateOwner Permission

    # def get_serializer(self, instance=None, data=None, partial=False):
    #     if self.request.method == 'PUT':
    #         return KitBuilderTemplateSerializer(instance=instance, data=data, partial=True)
    #     else:
    #         return KitBuilderTemplateSerializer(instance=instance, data=data, partial=partial)
