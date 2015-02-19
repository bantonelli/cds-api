from rest_framework import generics, permissions
from permissions import IsKitOwner, IsUser
from serializers import *
from provider.oauth2.models import AccessToken
from kitbuilder.models import Sale, Tag, KitDescription, Kit, Sample, CustomKit
from userprofile.models import UserProfile

User = get_user_model()


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
    permission_classes = (permissions.IsAuthenticated, )
    required_scopes = ['read']
    queryset = UserProfile.objects.all()
    serializer_class = UserProfilePublicSerializer

    def get_serializer_class(self, *args, **kwargs):
        current_user = self.request.user
        # if self.request.META['Authorization']:
        #     auth_header = self.request.META['Authorization']
        #     index = auth_header.find('Bearer') + 7
        #     token_string = auth_header[index:]
        #     token = AccessToken.objects.get_token(token=token_string)
        #     current_user = token.user
        user_id = self.kwargs.get(self.lookup_field)
        lookup_user = User.objects.get(pk=user_id)
        if lookup_user == current_user:
            return UserProfilePrivateSerializer
        else:
            return UserProfilePublicSerializer


import json
import stripe
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.context_processors import csrf


class CustomKitPaymentView(View):

    def get(self, request):
        # <view logic>
        result = []
        result.append({'csrf_token': unicode(csrf(request)['csrf_token'])})
        resp = HttpResponse(content_type="application/json")
        json.dump(result, resp)
        return resp

# Post request does the following:
    # 1) Get details about the kit.
    # 2) Calculate price of kit
    # 3) Create stripe charge
    # 4) Handle and respond with Stripe error message
    # 5) If Successful
        # 1) Build the Kit
        # 2) Save the Kit
        # 3) Email the user
    def post(self, request):

        stripe.api_key = settings.STRIPE_SECRET
        # Get the credit card details submitted by the form
        token = request.POST['stripeToken']

        err = "no errors"

        # Create the charge on Stripe's servers - this will charge the user's card
        try:
            charge = stripe.Charge.create(
            amount=1000, # amount in cents, again
            currency="usd",
            card=token,
            description="test@user.com"
        )
        except stripe.error.CardError, e:
        # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body['error']
            print "Status is: %s" % e.http_status
            print "Type is: %s" % err['type']
            print "Code is: %s" % err['code']
        # param is '' in this case
        #     print "Param is: %s" % err['param']
            print "Message is: %s" % err['message']
            err = err['message']
        except stripe.error.InvalidRequestError, e:
        # Invalid parameters were supplied to Stripe's API
            pass
        except stripe.error.AuthenticationError, e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
            pass
        except stripe.error.APIConnectionError, e:
        # Network communication with Stripe failed
            pass
        except stripe.error.StripeError, e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
            pass
        except Exception, e:
        # Something else happened, completely unrelated to Stripe
            pass

        success = True
        if err != "no errors":
            success = False
        else:
            success = True
            # build kit, email kit to user.
        result = []
        result.append({"success": success})
        result.append({"error": err})
        resp = HttpResponse(content_type="application/json")
        json.dump(result, resp)
        return resp