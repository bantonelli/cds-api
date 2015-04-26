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
    logo = serializers.ReadOnlyField(source='logo.url')

    class Meta:
        model = Vendor
        fields = ('id', 'name', 'website', 'logo', 'facebook', 'twitter', 'google_plus', 'soundcloud')


#-------------------------------------------------------------->
# VENDOR KIT
class VendorKitSerializer(serializers.ModelSerializer):
    samples = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    image = serializers.ReadOnlyField(source='image.url')
    tags = TagSerializer(read_only=True)

    class Meta:
        model = VendorKit
        fields = ('id', 'name', 'active', 'on_sale', 'soundcloud', 'image', 'description', 'sample_count', 'commission_rate', 'vendor', 'tags', 'price', 'sale', 'samples')


#-------------------------------------------------------------->
# SAMPLE SERIALIZERS
class SamplePreviewSerializer(serializers.ModelSerializer):
    preview = serializers.ReadOnlyField(source='preview.url')

    class Meta:
        model = Sample
        fields = ('id', 'name', 'type', 'bpm', 'duration', 'key', 'preview', 'vendor_kit')


class SampleSerializer(serializers.ModelSerializer):
    wav = serializers.ReadOnlyField(source='wav.url')

    class Meta:
        model = Sample
        fields = ('id', 'name', 'type', 'bpm', 'duration', 'key', 'wav', 'vendor_kit')


#-------------------------------------------------------------->
# KIT BUILDER PURCHASE
class KitBuilderPurchaseSerializer(serializers.ModelSerializer):
    samples = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = serializers.CharField(read_only=True, source='user.user.username')
    tags = TagSerializer(read_only=True)

    class Meta:
        model = KitBuilderPurchase
        fields = ('id', 'name', 'date_purchased', 'zip_file', 'samples', 'user')


#-------------------------------------------------------------->
# KIT BUILDER PURCHASE
class KitBuilderTemplateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True, source='user.user.username')
    samples = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tags = TagSerializer(read_only=True)
    image = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=False)

    def create(self, validated_data):
        return KitBuilderTemplate.objects.create(**validated_data)

    class Meta:
        model = KitBuilderTemplate
        fields = ('id', 'name', 'last_updated', 'times_added', 'featured', 'public', 'image', 'user', 'samples', 'tags')






