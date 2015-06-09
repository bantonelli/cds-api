__author__ = 'brandonantonelli'
# from kitbuilder.kitbuilder_v1.models import Sample
#
# sample = Sample.objects.get(pk=1)
# print sample.s3_preview_url

# from djoser.utils import SendEmailViewMixin
# from useraccount.models import User
# from kitbuilder.kitbuilder_v1.models import TemplateFollow

# user = User.objects.get(pk=1)
#
# print TemplateFollow.objects.get(user=user.id, template=1)

# Test Emails
# email_mixin = SendEmailViewMixin()
#
# email_mixin.send_email(**email_mixin.get_send_email_kwargs(user, 'account_activation'))

# print user.profile.samples_purchased

# from kitbuilder.kitbuilder_v1.models import Sample
#
# sample = Sample.objects.get(pk=1)
#
# import urllib
#
# urllib.urlretrieve(sample.s3_wav_url, "/tmp/" + sample.name + ".wav")


from django.core.files import File
from kitbuilder.kitbuilder_v1.models import KitBuilderPurchase

kb_purchase = KitBuilderPurchase.objects.get(pk=9)
kit_name = "Try Create template 2"

zip_file = kit_name + ".zip"

zip_to_upload = File(open(zip_file, 'rb'))
print zip_to_upload.name
print "with statement worked.."
# filename_to_save = kit_name + ".zip"
kb_purchase.zip_file.save(zip_file, zip_to_upload, True)
print "zip_file.save worked.."
kb_purchase.save()
print "Purchase Created! with zip attached!"