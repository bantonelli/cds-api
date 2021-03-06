from django.db import models
from django.conf import settings
#from django.contrib.auth import get_user_model
from useraccount.models import User
AuthUser = settings.AUTH_USER_MODEL
from amazon_file_field import S3EnabledImageField


#-------------------------------------------------------------->
# UTILITIES
def upload_profile_image(instance, filename):
    user_dir = "user_"+str(instance.user.id)
    #template_name = instance.name.replace(" ", "_").replace("'", "")
    return "media/user_profiles/" + user_dir + "/images/" + filename


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile")
    last_4_digits = models.CharField(max_length=4, blank=True)
    stripe_id = models.CharField(max_length=255, blank=True)
    subscribed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(blank=True, default=False)
    image = S3EnabledImageField(upload_to=upload_profile_image, blank=True)

    @property
    def username(self):
        "Expose User's username"
        # For use down the road we may need to access the username
        # through a user's profile
        return self.user.username

    @property
    def public_kitbuilder_templates(self):
        public_templates = self.kitbuilder_templates.filter(public=True)
        pub_template_ids = []
        for template in public_templates:
            pub_template_ids.append(template.id)
        return pub_template_ids

    @property
    def samples_purchased(self):
        samples = []
        for purchase in self.kitbuilder_purchases.all():
            samples.extend(purchase.samples.all())
        samples_purchased = set()
        for sample in samples:
            samples_purchased.add(sample.id)
        samples_purchased = list(samples_purchased)
        return samples_purchased

    def __unicode__(self):
        return self.user.username


User.get_or_create_profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

"""
We are defining a new property for the User model.
    The new property is called profile.
    Whenever you pass in a User object to this property it will get or create a UserProfile for this user.
    When we access the User object's profile property this code will get triggered and create a UserProfile that
    is linked to the User object.

ALSO:

1) Don't use get_user_model() in any models.py file
2) Use settings.AUTH_USER_MODEL when doing post_save() signals
    that reference Custom User model
3) Use get_user_model() in views and serializers.py
4) In Foreign Key fields use --> user = ForeignKey(settings.AUTH_USER_MODEL)
"""

# Access a User's profile by doing --> user_instance.profile
# Any changes made to it have to be saved
# use this to save--> user_instance.profile.save() method

from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver


@receiver(post_save, sender=AuthUser)
def user_save(sender, instance, **kwargs):
    instance.get_or_create_profile