from django.db import models
from userprofile.models import UserProfile
import os
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


class Price(CommonInfo):
    cost = models.DecimalField(max_digits=10, decimal_places=2)


class Sale(CommonInfo):
    percent_off = models.DecimalField(max_digits=10, decimal_places=2)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class KitDescription (CommonInfo):
    selling_point1 = models.TextField(blank=True)
    selling_point2 = models.TextField(blank=True)
    selling_point3 = models.TextField(blank=True)
    selling_point1_title = models.CharField(max_length=50, blank=True)
    selling_point2_title = models.CharField(max_length=50, blank=True)
    selling_point3_title = models.CharField(max_length=50, blank=True)
    number_of_samples = models.IntegerField(default=0)
    author = models.CharField(max_length=50, blank=True)
    date_created = models.CharField(max_length=50, blank=True)


class Kit (CommonInfo):
    new = models.BooleanField(default=True)
    on_sale = models.BooleanField(default=False)
    soundcloud = models.CharField(max_length=500)
    image = models.FileField(upload_to=upload_kit_image, storage=OverwriteStorage())
    tags = models.ManyToManyField(Tag)
    description = models.ForeignKey(KitDescription)
    price = models.ForeignKey(Price)
    sale = models.ForeignKey(Sale)
    user_rating = models.DecimalField(max_digits=5, decimal_places=4, default=0)


# Classes and Functions for Sample Model

def upload_sample_demo(instance, filename):
    kit_name = instance.kit.name.replace(" ", "_").replace("'", "")
    return "kits/" + kit_name + "/samples/demo/" + filename


def upload_sample(instance, filename):
    kit_name = instance.kit.name.replace(" ", "_").replace("'", "")
    return "kits/" + kit_name + "/samples/wav/" + filename


class Sample(models.Model):
    name = models.CharField(max_length=50)
    demo = models.FileField(upload_to=upload_sample_demo, storage=OverwriteStorage())
    wav = models.FileField(upload_to=upload_sample, storage=OverwriteStorage())
    kit = models.ForeignKey(Kit, related_name="samples")
    KICK = 'KD'
    SNARE = 'SD'
    CLAP = 'CP'
    OVERHEAD = 'OH'
    PERCUSSION = 'PC'
    SOUNDFX = 'FX'
    LOOP = 'LO'
    SAMPLE_TYPE_CHOICES = (
        (KICK, 'Kick'),
        (SNARE, 'Snare'),
        (CLAP, 'Clap'),
        (PERCUSSION, 'Percussion'),
        (SOUNDFX, 'Sound FX'),
        (LOOP, 'Loop'),
    )
    type = models.CharField(max_length=2, choices=SAMPLE_TYPE_CHOICES)

    def __unicode__(self):
        return self.name

# Classes and Functions for Custom Kit Model


class CustomKit(CommonInfo):
    user = models.ForeignKey(UserProfile, related_name='custom_kits')
    date = models.DateField(auto_now_add=True)
    samples = models.ManyToManyField(Sample)
    tags = models.ManyToManyField(Tag)


######## SIGNALS (for model deletion etc.)
# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


@receiver(pre_delete, sender=Sample)
def sample_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.demo.delete(False)
    instance.wav.delete(False)


@receiver(pre_delete, sender=Kit)
def kit_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.image.delete(False)







