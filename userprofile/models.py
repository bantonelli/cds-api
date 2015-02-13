from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.utils import timezone
from django.conf import settings
#Create your models here.


from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
                                password=password,
                                date_of_birth=date_of_birth
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin





# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True, db_index=True)
#     username = models.CharField(max_length=30)
#     date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#
#     objects = CustomUserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#
#     def __unicode__(self):
#         return self.email


# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile")
#     last_4_digits = models.CharField(max_length=4, blank=True)
#     stripe_id = models.CharField(max_length=255, blank=True)
#     subscribed = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
# settings.AUTH_USER_MODEL.get_or_create_profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
#
# """
# We are defining a new property for the User model.
#     The new property is called profile.
#     Whenever you pass in a User object to this property it will get or create a UserProfile for this user.
#     When we access the User object's profile property this code will get triggered and create a UserProfile that
#     is linked to the User object.
# """
#
# # Access a User's profile by doing --> user_instance.profile
# # Any changes made to it have to be saved
# # use this to save--> user_instance.profile.save() method
#
# from django.db.models.signals import post_save
# from django.dispatch.dispatcher import receiver
#
#
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def user_save(sender, instance, **kwargs):
#     instance.get_or_create_profile

