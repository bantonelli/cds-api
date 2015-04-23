__author__ = 'brandonantonelli'
# from django.conf import settings
from rest_framework import serializers
from kitbuilder.kitbuilder_v1.models import Tag, Vendor, VendorKit, Sample, KitBuilderPurchase, KitBuilderTemplate


#-------------------------------------------------------------->
# TAG
class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


#-------------------------------------------------------------->
# VENDOR
class VendorSerializer(serializers.ModelSerializer):
    logo = serializers.Field('logo.url')

    class Meta:
        model = Vendor
        fields = ('id', 'name', 'website', 'logo', 'facebook', 'twitter', 'google_plus', 'soundcloud')


#-------------------------------------------------------------->
# VENDOR KIT
class VendorKitSerializer(serializers.ModelSerializer):
    samples = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    image = serializers.Field('image.url')
    tags = TagSerializer(read_only=True)

    class Meta:
        model = VendorKit
        fields = ('id', 'name', 'active', 'on_sale', 'soundcloud', 'image', 'description', 'sample_count', 'commission_rate', 'vendor', 'tags', 'price', 'sale', 'samples')


#-------------------------------------------------------------->
# SAMPLE SERIALIZERS
class SamplePreviewSerializer(serializers.ModelSerializer):
    preview = serializers.Field('preview.url')

    class Meta:
        model = Sample
        fields = ('id', 'name', 'type', 'bpm', 'duration', 'key', 'preview', 'vendor_kit')


class SampleSerializer(serializers.ModelSerializer):
    wav = serializers.Field('wav.url')

    class Meta:
        model = Sample
        fields = ('id', 'name', 'type', 'bpm', 'duration', 'key', 'wav', 'vendor_kit')


#-------------------------------------------------------------->
# KIT BUILDER PURCHASE
class KitBuilderPurchaseSerializer(serializers.ModelSerializer):
    samples = serializers.PrimaryKeyRelatedField(many=True)
    user = serializers.CharField(read_only=True, source='user.user.username')
    tags = TagSerializer(read_only=True)

    class Meta:
        model = KitBuilderPurchase
        fields = ('id', 'name', 'date_purchased', 'zip_file', 'samples', 'user')


#-------------------------------------------------------------->
# KIT BUILDER PURCHASE
class KitBuilderTemplateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True, source='user.user.username')
    samples = serializers.PrimaryKeyRelatedField(many=True)
    tags = TagSerializer(read_only=True)

    class Meta:
        model = KitBuilderTemplate
        fields = ('id', 'name', 'last_updated', 'times_added', 'featured', 'public', 'image', 'user', 'samples', 'tags')






