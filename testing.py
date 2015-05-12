__author__ = 'brandonantonelli'
# from kitbuilder.kitbuilder_v1.models import Sample
#
# sample = Sample.objects.get(pk=1)
# print sample.s3_preview_url

from djoser.utils import SendEmailViewMixin
from useraccount.models import User

user = User.objects.get(pk=15)

email_mixin = SendEmailViewMixin()

email_mixin.send_email(**email_mixin.get_send_email_kwargs(user))