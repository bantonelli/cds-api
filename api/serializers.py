__author__ = 'brandonantonelli'

from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
from kitbuilder.models import Sale, Tag, KitDescription, Kit, Sample, CustomKit
from userprofile.models import UserProfile


# KIT BUILDER
class SampleDemoSerializer(serializers.ModelSerializer):
    demo = serializers.Field('demo.url')

    class Meta:
        model = Sample
        fields = ('id', 'name', 'demo', 'kit', 'type')


class SampleSerializer(serializers.ModelSerializer):
    demo = serializers.Field('demo.url')

    class Meta:
        model = Sample
        fields = ('id', 'name', 'demo', 'wav', 'kit', 'type')


class KitDescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = KitDescription
        fields = ('id', 'selling_point1', 'selling_point2', 'selling_point3', 'selling_point1_title', 'selling_point2_title', 'selling_point3_title', 'number_of_samples', 'author', 'date_created')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class KitSerializer(serializers.ModelSerializer):
    samples = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    description = KitDescriptionSerializer(read_only=True)
    image = serializers.Field('image.url')
    tags = TagSerializer(read_only=True)

    class Meta:
        model = Kit
        fields = ('id', 'name', 'new', 'on_sale', 'soundcloud', 'image', 'tags', 'description', 'price', 'sale', 'user_rating', 'samples')


class CustomKitSerializer(serializers.ModelSerializer):
    samples = serializers.PrimaryKeyRelatedField(many=True)
    user = serializers.CharField(read_only=True, source='user.user.username')
    tags = TagSerializer(read_only=True)

    class Meta:
        model = CustomKit
        fields = ('id', 'name', 'user', 'date', 'samples', 'tags')


class CustomKitPurchasedSerializer(serializers.ModelSerializer):
    samples = serializers.PrimaryKeyRelatedField(many=True)
    user = serializers.CharField(read_only=True, source='user.user.username')
    tags = TagSerializer(read_only=True)

    class Meta:
        model = CustomKit
        fields = ('id', 'name', 'user', 'date', 'samples', 'tags')


#USER PROFILE
class UserProfilePrivateSerializer(serializers.ModelSerializer):
    # Needs Object level permission
    custom_kits = CustomKitPurchasedSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'last_4_digits', 'created_at', 'updated_at', 'custom_kits')


class UserProfilePublicSerializer(serializers.ModelSerializer):
    custom_kits = CustomKitPurchasedSerializer(many=True, read_only=True)
    username = serializers.Field()

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'created_at', 'updated_at', 'custom_kits')



