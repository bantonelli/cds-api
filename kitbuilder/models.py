from django.db import models
from userprofile.models import UserProfile
import os
from datetime import date
from django.conf import settings
from django.core.files.storage import FileSystemStorage


User = settings.AUTH_USER_MODEL

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


# Classes and Functions for Kit Model

def upload_kit_image(instance, filename):
    kit_name = instance.name.replace(" ", "_").replace("'", "")
    return "kits/" + kit_name + "/" + filename


class CommonInfo(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


# Classes and Functions for Sample Model

def upload_sample_demo(instance, filename):
    kit_name = instance.kit.name.replace(" ", "_").replace("'", "")
    return "kits/" + kit_name + "/samples/demo/" + filename


def upload_sample(instance, filename):
    kit_name = instance.kit.name.replace(" ", "_").replace("'", "")
    return "kits/" + kit_name + "/samples/wav/" + filename


######## SIGNALS (for model deletion etc.)
# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver





