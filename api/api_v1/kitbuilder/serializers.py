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
    preview = serializers.ReadOnlyField(source='s3_preview_url')

    class Meta:
        model = Sample
        fields = ('id', 'name', 'type', 'bpm', 'duration', 'key', 'preview', 'vendor_kit')


class SampleSerializer(serializers.ModelSerializer):
    wav = serializers.ReadOnlyField(source='s3_wav_url')

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
    name = serializers.CharField(required=False)
    user = serializers.CharField(read_only=True, source='user.user.username')
    image = serializers.ImageField(allow_empty_file=True, required=False, max_length=None)

    def create(self, validated_data):
        user = validated_data.get('user')
        name = validated_data.get('name')
        public = validated_data.get('public')
        if public is None:
            public = False
        image = validated_data.get('image')
        samples = validated_data.get('samples')
        tags = validated_data.get('tags')
        template = KitBuilderTemplate(
            user=user,
            name=name,
            public=public,
        )
        template.save()
        template.image = image
        template.save()
        for tag in tags:
            template.tags.add(tag)
        for sample in samples:
            template.samples.add(sample)
        template.save()
        return template

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




