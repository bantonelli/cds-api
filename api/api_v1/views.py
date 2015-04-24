__author__ = 'brandonantonelli'
import os
import zipfile
import ast
import json
import stripe
from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from .kitbuilder.views import Sample, KitBuilderPurchase
from .userprofile.views import UserProfile
# from provider.oauth2.models import AccessToken
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from django.core.context_processors import csrf

User = get_user_model()


# Post request does the following:
    # 1) Get details about the kit.
    # 2) Calculate price of kit
    # 3) Create stripe charge
    # 4) Handle and respond with Stripe error message
    # 5) If Successful
        # 1) Build the Kit
        # 2) Save the Kit
        # 3) Email the user
class KitBuilderPaymentView(View):

    def post(self, request):
        result = []
        payment_success = None
        payment_error = "no errors"
        zip_created = None
        mail_sent = None
        order_number = None
        purchased_kit_id = None

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

        if kit_name == "":
            result.append({"data_error": "You have not entered a name for your custom kit!"})
            resp = HttpResponse(content_type="application/json")
            json.dump(result, resp)
            return resp

        if len(samples) <= 0:
            result.append({"data_error": "You have not chosen any samples!"})
            resp = HttpResponse(content_type="application/json")
            json.dump(result, resp)
            return resp

        users_custom_kits = user.profile.custom_kits.all()
        if users_custom_kits.filter(name=kit_name).exists():
            result.append({"data_error": "You already have a custom kit with that name!"})
            resp = HttpResponse(content_type="application/json")
            json.dump(result, resp)
            return resp

        charge_amount = int((len(samples) * 100) * 0.50)
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
            body = e.json_body
            err = body['error']
            payment_error = err['message']
        except stripe.error.AuthenticationError, e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
            body = e.json_body
            err = body['error']
            payment_error = err['message']
        except stripe.error.APIConnectionError, e:
        # Network communication with Stripe failed
            body = e.json_body
            err = body['error']
            payment_error = err['message']
        except stripe.error.StripeError, e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
            body = e.json_body
            err = body['error']
            payment_error = err['message']
        except Exception, e:
        # Something else happened, completely unrelated to Stripe
            payment_error = "There was an error processing your payment."

        if payment_error != "no errors":
            payment_success = False
        else:
        # build kit zip file --> DONE
        # create custom kit object and associate with User --> DONE
        # email kit to user --> DONE
            payment_success = True
            order_number = charge.id
            try:
                sample_objects = []
                for sample in samples:
                    # Try to get sample. If it doesn't exist pass.
                    try:
                        sample_objects.append(Sample.objects.get(pk=sample))
                    except ObjectDoesNotExist:
                        pass
                #Build a path for the zip file that is inside of a folder that holds user-specific custom kit zips
                zip_subdir = kit_name
                zip_filepath = os.path.join(settings.MEDIA_ROOT, "kitbuilder_purchases", "user_"+str(user_id))

                # If the user's zip file folder doesn't exist create one
                if not os.path.exists(zip_filepath):
                    os.makedirs(zip_filepath)

                # Create the location for the zip file and the extension
                zip_file = os.path.join(zip_filepath, "%s.zip" % zip_subdir)
                # Build the media hosted URL path for the zip file (where it can be downloaded)
                zip_media_path = os.path.join(settings.MEDIA_URL[0:-1], "kitbuilder_purchases", "user_"+str(user_id), "%s.zip" % zip_subdir)
                # The zip compressor makes an open zip file buffer ready to be written to.
                zf = zipfile.ZipFile(zip_file, mode='w')

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
                    custom_kit = KitBuilderPurchase(name=kit_name, user=user_profile, zip_file=zip_media_path)
                    custom_kit.save()
                    # Associate samples with custom kit object
                    custom_kit.samples = sample_objects
                    custom_kit.save()
                    purchased_kit_id = custom_kit.id
                except:
                    return "Custom Kit Creation Error"
                try:
                    email = user.email
                    mail = EmailMessage("Your Recent KitBuilder Purchase", "Here is your custom Kit", "bant7205@gmail.com", [email])
                    mail.attach_file(zip_file)
                    mail.send()
                    mail_sent = True
                except:
                    mail_sent = False
                    return "Attachment error"
            except:
                zip_created = False
                return "Zip File Error"

        result.append({
            "purchased_kit_id": purchased_kit_id,
            "order_number": order_number,
            "payment_success": payment_success,
            "payment_error": payment_error,
            "zip_created": zip_created,
            "mail_sent": mail_sent
        })
        #result.append({"samples": samples[0]})
        resp = HttpResponse(content_type="application/json")
        json.dump(result, resp)
        return resp