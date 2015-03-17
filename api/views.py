import os
import zipfile
import StringIO
import ast
import cgi

from rest_framework import generics, permissions
from permissions import IsKitOwner, IsUser
from serializers import *
from provider.oauth2.models import AccessToken
from kitbuilder.models import Sale, Tag, KitDescription, Kit, Sample, CustomKit
from userprofile.models import UserProfile
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.core.exceptions import ObjectDoesNotExist

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


# Post request does the following:
    # 1) Get details about the kit.
    # 2) Calculate price of kit
    # 3) Create stripe charge
    # 4) Handle and respond with Stripe error message
    # 5) If Successful
        # 1) Build the Kit
        # 2) Save the Kit
        # 3) Email the user
class CustomKitPaymentView(View):

    def get(self, request):
        # <view logic>
        result = []
        result.append({'csrf_token': unicode(csrf(request)['csrf_token'])})
        resp = HttpResponse(content_type="application/json")
        json.dump(result, resp)
        return resp

    def post(self, request):
        result = []
        payment_success = None
        payment_error = "no errors"
        zip_created = None
        mail_sent = None

        # Get the credit card details submitted by the form
        token = request.POST['stripeToken']
        user_id = request.POST['userID']
        kit_name = request.POST['kitName']
        samples = request.POST['samples']
        samples = ast.literal_eval(samples)

        stripe.api_key = settings.STRIPE_SECRET
        # Check for user input / post data errors
        user = None
        try:
            user = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            result.append({"data_error": "user is invalid"})
            resp = HttpResponse(content_type="application/json")
            json.dump(result, resp)
            return resp

        users_custom_kits = user.profile.custom_kits.all()
        if users_custom_kits.filter(name=kit_name).exists():
            result.append({"data_error": "You already have a custom kit with that name!"})
            resp = HttpResponse(content_type="application/json")
            json.dump(result, resp)
            return resp

        charge_amount = int((len(samples) * 100) * 0.75)
        # Create the charge on Stripe's servers - this will charge the user's card
        try:
            charge = stripe.Charge.create(
            amount=charge_amount, # amount in cents, again
            currency="usd",
            card=token,
            description=user.email
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
            payment_error = err['message']
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
            payment_error = "There was an error processing your payment."
            pass

        if payment_error != "no errors":
            payment_success = False
        else:
        # build kit zip file --> DONE
        # create custom kit object and associate with User --> DONE
        # email kit to user --> DONE
            payment_success = True
            try:
                sample_objects = []
                for sample in samples:
                    # Try to get sample. If it doesn't exist pass.
                    try:
                        sample_objects.append(Sample.objects.get(pk=sample))
                    except ObjectDoesNotExist:
                        pass

                zip_subdir = kit_name
                zip_filepath = os.path.join(settings.MEDIA_ROOT, "custom_kits", "user_"+str(user_id))
                if not os.path.exists(zip_filepath):
                    os.makedirs(zip_filepath)
                zip_filename = os.path.join(zip_filepath, "%s.zip" % zip_subdir)
                zip_media_path = os.path.join(settings.MEDIA_URL[0:-1], "custom_kits", "user_"+str(user_id), "%s.zip" % zip_subdir)
                # The zip compressor
                zf = zipfile.ZipFile(zip_filename, mode='w')

                for sample in sample_objects:
                    # Calculate path for file in zip
                    fpath = sample.wav.url[1:]
                    fpath = os.path.join(settings.BASE_DIR, fpath)
                    fname = os.path.basename(fpath)
                    zip_path = os.path.join(zip_subdir, sample.type, fname)
                    # Add file, at correct path
                    zf.write(fpath, zip_path)

                # Must close zip for all contents to be written
                zf.close()
                zip_created = True
                try:
                    # Create Custom Kit object, associate with User Profile and Zip file
                    user_profile = UserProfile.objects.get(pk=user_id)
                    custom_kit = CustomKit(name=kit_name, user=user_profile, zip_file=zip_media_path)
                    custom_kit.save()
                    # Associate samples with custom kit object
                    custom_kit.samples = sample_objects
                    custom_kit.save()
                except:
                    return "Custom Kit Creation Error"
                try:
                    email = user.email
                    mail = EmailMessage("Your Custom Kit", "Here is your custom Kit", "bant7205@gmail.com", [email])
                    mail.attach_file(zip_filename)
                    mail.send()
                    mail_sent = True
                except:
                    mail_sent = False
                    return "Attachment error"
            except:
                zip_created = False
                return "Zip File Error"

        result.append({"payment_success": payment_success})
        result.append({"payment_error": payment_error})
        result.append({"zip_created": zip_created})
        result.append({"mail_sent": mail_sent})
        #result.append({"samples": samples[0]})
        resp = HttpResponse(content_type="application/json")
        json.dump(result, resp)
        return resp