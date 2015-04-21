from django.db import models
from userprofile.models import UserProfile
import os
from datetime import date
from django.conf import settings
from django.core.files.storage import FileSystemStorage


#-------------------------------------------------------------->
# UTILITIES

User = settings.AUTH_USER_MODEL

# This class is used to create the file system storage used for files on OS.
# It checks if the file exists and overwrites the file if it exists.
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


#-------------------------------------------------------------->
# VENDOR KIT

def upload_vendor_logo(instance, filename):
    vendor_name = instance.name.replace(" ", "_").replace("'", "")
    return "vendors/" + vendor_name + "/logo/" + filename


def upload_vendor_kit_image(instance, filename):
    kit_name = instance.name.replace(" ", "_").replace("'", "")
    return "vendor_kits/" + kit_name + "/" + filename


class Vendor(CommonInfo):
    website = models.URLField(blank=True, null=True)
#    description = models.ForeignKey(KitDescription) # This should be a WYSIWYG field
    logo = models.FileField(upload_to=upload_vendor_kit_image, storage=OverwriteStorage())
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    google_plus = models.URLField(blank=True, null=True)
    soundcloud = models.URLField(blank=True, null=True)


class VendorKit (CommonInfo):
    active = models.BooleanField(default=True)
    on_sale = models.BooleanField(default=False)
    soundcloud = models.CharField(max_length=500)
    image = models.FileField(upload_to=upload_vendor_kit_image, storage=OverwriteStorage())
#    description = models.ForeignKey(KitDescription) # This should be a WYSIWYG field
    sample_count = models.IntegerField(blank=True, null=True)
    commission_rate = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.ForeignKey(Vendor)
    tags = models.ManyToManyField(Tag)
    price = models.ForeignKey(Price)
    sale = models.ForeignKey(Sale)


#-------------------------------------------------------------->
# SAMPLE

def upload_sample_preview(instance, filename):
    kit_name = instance.kit.name.replace(" ", "_").replace("'", "")
    return "vendor_kits/" + kit_name + "/samples/preview/" + filename


def upload_sample_wav(instance, filename):
    kit_name = instance.kit.name.replace(" ", "_").replace("'", "")
    return "vendor_kits/" + kit_name + "/samples/wav/" + filename


class Sample(models.Model):
    KICK = 'Kick'
    SNARE = 'Snare'
    CLAP = 'Clap'
    OVERHEAD = 'Overhead'
    PERCUSSION = 'Percussion'
    SOUNDFX = 'Sound FX'
    LOOP = 'Loop'
    SAMPLE_TYPE_CHOICES = (
        (KICK, 'Kick'),
        (SNARE, 'Snare'),
        (CLAP, 'Clap'),
        (OVERHEAD, 'Overhead'),
        (PERCUSSION, 'Percussion'),
        (SOUNDFX, 'Sound FX'),
        (LOOP, 'Loop'),
    )
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=SAMPLE_TYPE_CHOICES)
    bpm = models.IntegerField(default=0, blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)  # add this field when updating to 1.8
    key = models.CharField(max_length=10, blank=True, null=True)
    preview = models.FileField(upload_to=upload_sample_preview, storage=OverwriteStorage())
    wav = models.FileField(upload_to=upload_sample_wav, storage=OverwriteStorage())
    vendor_kit = models.ForeignKey(VendorKit, related_name="samples")

    def __unicode__(self):
        return self.name


#-------------------------------------------------------------->
# KIT BUILDER PURCHASE

class KitBuilderPurchase(models.Model):
    name = models.CharField(max_length=100)
    date_purchased = models.DateField(auto_now_add=True)
    zip_file = models.FilePathField(blank=True, null=True, max_length=250)
    samples = models.ManyToManyField(Sample, blank=True)
    user = models.ForeignKey(UserProfile, related_name='kitbuilder_purchases')

    def __unicode__(self):
        return self.name


#-------------------------------------------------------------->
# KIT BUILDER TEMPLATE

def upload_template_image(instance, filename):
    user_dir = "user_"+str(instance.user.id)
    template_name = instance.name.replace(" ", "_").replace("'", "")
    return "kb_templates/" + user_dir + "/" + template_name + "/" + filename


class KitBuilderTemplate(models.Model):
    name = models.CharField(max_length=100)
    last_updated = models.DateField(auto_now=True)
    purchases = models.IntegerField(default=0)
#    description = models.ForeignKey(KitDescription) # This should be a WYSIWYG field
    featured = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    image = models.FileField(upload_to=upload_template_image, storage=OverwriteStorage())
    user = models.ForeignKey(UserProfile, related_name='kitbuilder_templates')
    samples = models.ManyToManyField(Sample, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __unicode__(self):
        return self.name

#-------------------------------------------------------------->
# KIT BUILDER TEMPLATE

######## SIGNALS (for model deletion etc.)
# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


@receiver(pre_delete, sender=Sample)
def sample_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.preview.delete(False)
    instance.wav.delete(False)


@receiver(pre_delete, sender=VendorKit)
def vendor_kit_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.image.delete(False)


@receiver(pre_delete, sender=KitBuilderPurchase)
def kitbuilder_purchase_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    zip_filename = instance.name
    user_id = instance.user.id
    zip_filepath = os.path.join(settings.MEDIA_ROOT, "kitbuilder_purchases", "user_"+str(user_id), "%s.zip" % zip_filename)
    try:
        os.remove(zip_filepath)
    except OSError:
        pass


@receiver(pre_delete, sender=KitBuilderTemplate)
def kitbuilder_template_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.image.delete(False)



# DROP TABLE "kitbuilder_v1_kitbuildertemplate" CASCADE;
# DROP TABLE "kitbuilder_v1_kitbuildertemplate_samples" CASCADE;
# DROP TABLE "kitbuilder_v1_kitbuildertemplate_tags" CASCADE;
# DROP TABLE "kitbuilder_v1_kitbuilderpurchase" CASCADE;
# DROP TABLE "kitbuilder_v1_kitbuilderpurchase_samples" CASCADE;
# DROP TABLE "kitbuilder_v1_sample" CASCADE;
# DROP TABLE "kitbuilder_v1_vendorkit" CASCADE;
# DROP TABLE "kitbuilder_v1_vendorkit_tags" CASCADE;
# DROP TABLE "kitbuilder_v1_vendor" CASCADE;
# DROP TABLE "kitbuilder_v1_tag" CASCADE;
# DROP TABLE "kitbuilder_v1_sale" CASCADE;
# DROP TABLE "kitbuilder_v1_price" CASCADE;