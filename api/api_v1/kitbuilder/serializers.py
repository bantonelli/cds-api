__author__ = 'brandonantonelli'
# from django.conf import settings
from rest_framework import serializers
from kitbuilder.kitbuilder_v1.models import Tag, Sale, Price, Vendor, VendorKit, Sample, KitBuilderPurchase, KitBuilderTemplate


#-------------------------------------------------------------->
# PRICE
class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = ('id', 'name', 'cost')


#-------------------------------------------------------------->
# SALE
class SaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sale
        fields = ('id', 'name', 'percent_off')


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
# SAMPLE SERIALIZERS
class SamplePreviewSerializer(serializers.ModelSerializer):
    preview = serializers.ReadOnlyField(source='s3_preview_url')

    class Meta:
        model = Sample
        fields = ('id', 'name', 'type', 'bpm', 'key', 'preview', 'vendor_kit')


class SampleSerializer(serializers.ModelSerializer):
    wav = serializers.ReadOnlyField(source='s3_wav_url')

    class Meta:
        model = Sample
        fields = ('id', 'name', 'type', 'bpm', 'key', 'wav', 'vendor_kit')


#-------------------------------------------------------------->
# VENDOR KIT
class VendorKitSerializer(serializers.ModelSerializer):
    samples = SamplePreviewSerializer(many=True, read_only=True)
    image = serializers.ReadOnlyField(source='image.url')
    tags = TagSerializer(read_only=True)
    price = PriceSerializer(read_only=True)
    sale = SaleSerializer(read_only=True)

    class Meta:
        model = VendorKit
        fields = ('id', 'name', 'active', 'on_sale', 'soundcloud', 'image', 'description', 'sample_count', 'commission_rate', 'vendor', 'tags', 'price', 'sale', 'samples')


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
    name = serializers.CharField(required=False)
    user = serializers.CharField(read_only=True, source='user.user.username')
    image = serializers.ImageField(allow_empty_file=True, required=False, max_length=None)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.public = validated_data.get('public', instance.public)
        instance.image = validated_data.get('image', instance.image)
        instance.samples = validated_data.get('samples', instance.samples)
        instance.tags = validated_data.get('tags', instance.tags)
        instance.save()
        return instance

    class Meta:
        model = KitBuilderTemplate
        fields = ('id', 'name', 'last_updated', 'times_added', 'description', 'featured', 'public', 'image', 'user', 'samples', 'tags')
        read_only_fields = ('times_added', 'last_updated', 'featured',)




