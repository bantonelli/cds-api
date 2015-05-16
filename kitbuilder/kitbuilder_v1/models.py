from django.db import models
from userprofile.models import UserProfile
import os
from datetime import date
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from tinymce.models import HTMLField
from amazon_file_field import S3Storage, S3EnabledImageField
from boto.s3.key import Key
from boto.s3.connection import S3Connection
#-------------------------------------------------------------->
# UTILITIES


def get_bucket():
    if settings.USE_AMAZON_S3:
        bucket = settings.AWS_STORAGE_BUCKET_NAME
        connection = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        if not connection.lookup(bucket):
            connection.create_bucket(bucket)
        bucket = connection.get_bucket(bucket)
        return bucket

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
    return "media/vendors/" + vendor_name + "/logo/" + filename

def upload_vendor_kit_image(instance, filename):
    vendor_name = instance.vendor.name.replace(" ", "_").replace("'", "")
    kit_name = instance.name.replace(" ", "_").replace("'", "")
    return "media/vendors/" + vendor_name + "/kits/" + kit_name + "/" + filename


class Vendor(CommonInfo):
    website = models.URLField(blank=True, null=True)
#    description = models.ForeignKey(KitDescription) # This should be a WYSIWYG field
#     logo = models.ImageField(upload_to=upload_vendor_logo, storage=S3Storage(get_bucket()))
    logo = S3EnabledImageField(upload_to=upload_vendor_logo)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    google_plus = models.URLField(blank=True, null=True)
    soundcloud = models.URLField(blank=True, null=True)


class VendorKit (CommonInfo):
    active = models.BooleanField(default=True)
    on_sale = models.BooleanField(default=False)
    soundcloud = models.CharField(max_length=500)
    # image = models.ImageField(upload_to=upload_vendor_kit_image, storage=S3Storage(get_bucket()))
    image = S3EnabledImageField(upload_to=upload_vendor_kit_image)
    description = HTMLField(blank=True) # This should be a WYSIWYG field
    sample_count = models.IntegerField(blank=True, null=True)
    commission_rate = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.ForeignKey(Vendor)
    tags = models.ManyToManyField(Tag)
    price = models.ForeignKey(Price)
    sale = models.ForeignKey(Sale)


#-------------------------------------------------------------->
# SAMPLE

def upload_sample_preview(instance, filename):
    vendor_name = instance.vendor_kit.vendor.name.replace(" ", "_").replace("'", "")
    kit_name = instance.vendor_kit.name.replace(" ", "_").replace("'", "")
    return "media/vendors/" + vendor_name + "/kits/" + kit_name + "/samples/preview/" + filename


def upload_sample_wav(instance, filename):
    vendor_name = instance.vendor_kit.vendor.name.replace(" ", "_").replace("'", "")
    kit_name = instance.vendor_kit.name.replace(" ", "_").replace("'", "")
    return "media/vendors/" + vendor_name + "/kits/" + kit_name + "/samples/wav/" + filename


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
    key = models.CharField(max_length=10, blank=True, null=True)
    preview = models.TextField()
    wav = models.TextField()
    vendor_kit = models.ForeignKey(VendorKit, related_name="samples")
    bucket = get_bucket()

    @property
    def s3_preview_url(self):
        return Key(self.bucket, self.preview).generate_url(100000)

    @property
    def s3_wav_url(self):
        return Key(self.bucket, self.wav).generate_url(100000)

    def __unicode__(self):
        return self.name


#-------------------------------------------------------------->
# KIT BUILDER PURCHASE

class KitBuilderPurchase(models.Model):
    name = models.CharField(max_length=100)
    date_purchased = models.DateField(auto_now_add=True)
    zip_file = models.FilePathField(blank=True, null=True, max_length=250) # Change this to URL FIELD and ADD COMPUTED PROPERTY
    samples = models.ManyToManyField(Sample, blank=True)
    user = models.ForeignKey(UserProfile, related_name='kitbuilder_purchases')

    def __unicode__(self):
        return self.name


#-------------------------------------------------------------->
# KIT BUILDER TEMPLATE

def upload_template_image(instance, filename):
    user_dir = "user_"+str(instance.user.id)
    #template_name = instance.name.replace(" ", "_").replace("'", "")
    template_id = instance.id
    return "media/kb_templates/" + user_dir + "/" + str(template_id) + "/" + filename


class KitBuilderTemplate(models.Model):
    name = models.CharField(max_length=100)
    last_updated = models.DateField(auto_now=True)
    times_added = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    # image = models.ImageField(upload_to=upload_template_image, storage=S3Storage(get_bucket()), blank=True, null=True)
    image = S3EnabledImageField(upload_to=upload_template_image)
    user = models.ForeignKey(UserProfile, related_name='kitbuilder_templates')
    samples = models.ManyToManyField(Sample, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    followers = models.ManyToManyField(
        UserProfile,
        blank=True,
        related_name="templates_followed",
        through="Follower",
        through_fields=('template', 'user')
    )

    def __unicode__(self):
        return self.name


class Follower(models.Model):
    template = models.ForeignKey(KitBuilderTemplate)
    user = models.ForeignKey(UserProfile)
    date_followed = models.DateField(auto_now_add=True)
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