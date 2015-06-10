__author__ = 'brandonantonelli'
import os
import zipfile
import urllib2
import ast
import json
import stripe
from django.core.files import File
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


try:
    from cStringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO


class InMemoryZip(object):
    def __init__(self):
        # Create the in-memory file-like object
        self.in_memory_data = StringIO()
        # Create the in-memory zipfile
        self.in_memory_zip = zipfile.ZipFile(
            self.in_memory_data, "w", zipfile.ZIP_DEFLATED, False)
        self.in_memory_zip.debug = 3

    def append(self, filename_in_zip, file_contents):
        '''Appends a file with name filename_in_zip and contents of
        file_contents to the in-memory zip.'''
        self.in_memory_zip.writestr(filename_in_zip, file_contents)
        return self   # so you can daisy-chain

    def writetofile(self, filename):
        '''Writes the in-memory zip to a file.'''
        # Mark the files as having been created on Windows so that
        # Unix permissions are not inferred as 0000
        for zfile in self.in_memory_zip.filelist:
            zfile.create_system = 0
        self.in_memory_zip.close()
        with open(filename, 'wb') as f:
            f.write(self.in_memory_data.getvalue())


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

        user_purchases = user.profile.kitbuilder_purchases.all()
        if user_purchases.filter(name=kit_name).exists():
            result.append({"data_error": "You have already purchased a template with that name!"})
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
        # create kitbuilder_purchase object and associate with User --> DONE
            # NEW --> Upload the kitbuilder_purchase to S3 and create download link for it. DONE
        # email kit to user --> DONE
            payment_success = True
            print payment_success
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
                # zip_subdir = kit_name
                # zip_filepath = os.path.join("media", "kitbuilder_purchases", "user_"+str(user_id))
                #
                # # If the user's zip file folder doesn't exist create one
                # if not os.path.exists(zip_filepath):
                #     os.makedirs(zip_filepath)
                #
                # # Create the location for the zip file and the extension
                # zip_file = os.path.join(zip_filepath, "%s.zip" % zip_subdir)
                # # Build the media hosted URL path for the zip file (where it can be downloaded)
                # zip_media_path = os.path.join(settings.MEDIA_URL[0:-1], "kitbuilder_purchases", "user_"+str(user_id), "%s.zip" % zip_subdir)
                # # The zip compressor makes an open zip file buffer ready to be written to.
                # zip_file = kit_name + ".zip"
                # zf = zipfile.ZipFile(zip_file, mode='w')
                #
                # for sample in sample_objects:
                #     # Calculate path for file in zip
                #     fpath = sample.wav.url[1:]
                #     fpath = os.path.join(settings.BASE_DIR, fpath)
                #     fname = os.path.basename(fpath)
                #     zip_path = os.path.join(zip_subdir, sample.type, fname)
                #     # Add file, at correct path
                #     #     fpath is the path to the wav.
                #     zf.write(fpath, zip_path)
                #
                # # Must close zip for all contents to be written
                # zf.close()

                imz = InMemoryZip()
                zip_file = kit_name + ".zip"
                for sample in sample_objects:
                    sample_url = sample.s3_wav_url
                    sample_name = sample.name + ".wav"
                    sample_sub_path = sample.type + 's'
                    zip_path = os.path.join(kit_name, sample_sub_path, sample_name)
                    response = urllib2.urlopen(sample_url)
                    imz.append(zip_path, response.read())

                imz.writetofile(zip_file)
                zip_created = True
                print zip_created
                try:
                    # Create Custom Kit object, associate with User Profile and Zip file
                    user_profile = UserProfile.objects.get(pk=user_id)
                    kb_purchase = KitBuilderPurchase(name=kit_name, user=user_profile)
                    kb_purchase.save()
                    # Associate samples with custom kit object
                    kb_purchase.samples = sample_objects
                    kb_purchase.save()
                    purchased_kit_id = kb_purchase.id
                    zip_to_upload = File(open(zip_file, 'rb'))
                    print zip_to_upload.name
                    print "with statement worked.."
                    # filename_to_save = kit_name + ".zip"
                    kb_purchase.zip_file.save(zip_file, zip_to_upload, True)
                    print "zip_file.save worked.."
                    kb_purchase.save()
                    print "Purchase Created! with zip attached!"
                except:
                    print "Kb Purchase Not created"
                    # return "Custom Kit Creation Error"
                    pass
                try:
                    email = user.email
                    body_text = "Thank you for purchasing a custom kit from BeatParadigm. Log in to your account, and check account settings at any time to download your purchase. Your order number: " + order_number + ". Amount paid: $" + str(charge_amount/100) + ".",
                    mail = EmailMessage("Your Recent KitBuilder Purchase", body_text, "sales@beatparadigm.com", [email])
                    # mail.attach_file(zip_file)
                    mail.send()
                    mail_sent = True
                except:
                    mail_sent = False
                    print "Mail not being sent"
                    # return "Attachment error"
                    pass
                # Delete the local zip file after it is sent.
                os.remove(zip_file)
            except:
                zip_created = False
                print "Zip File Error"
                pass


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