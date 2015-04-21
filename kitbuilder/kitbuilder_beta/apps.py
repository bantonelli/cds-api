from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AuthConfig(AppConfig):
    name = 'kitbuilder.beta'
    verbose_name = _("KitBuilder Beta")


