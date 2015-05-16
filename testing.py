__author__ = 'brandonantonelli'
# from kitbuilder.kitbuilder_v1.models import Sample
#
# sample = Sample.objects.get(pk=1)
# print sample.s3_preview_url

from djoser.utils import SendEmailViewMixin
from useraccount.models import User
from kitbuilder.kitbuilder_v1.models import Follower

user = User.objects.get(pk=1)

print Follower.objects.get(user=user.id, template=1)

# Test Emails
# email_mixin = SendEmailViewMixin()
#
# email_mixin.send_email(**email_mixin.get_send_email_kwargs(user, 'account_activation'))

# print user.profile.samples_purchased
