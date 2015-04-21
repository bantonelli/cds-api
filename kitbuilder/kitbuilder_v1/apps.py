from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AuthConfig(AppConfig):
    name = 'kitbuilder.v1'
    verbose_name = _("KitBuilder Version 1")


