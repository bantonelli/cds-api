from rest_framework import serializers
from userprofile.models import UserProfile
from api.api_v1.kitbuilder.serializers import KitBuilderPurchaseSerializer, KitBuilderTemplateSerializer


#-------------------------------------------------------------->
# USER PROFILE
class UserProfilePrivateSerializer(serializers.ModelSerializer):
    # Needs Object level permission
    kitbuilder_purchases = KitBuilderPurchaseSerializer(many=True, read_only=True)
    kitbuilder_templates = KitBuilderTemplateSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.kitbuilder_templates = validated_data.get('kitbuilder_templates', instance.kitbuilder_templates)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'image', 'last_4_digits', 'stripe_id', 'created_at', 'updated_at', 'kitbuilder_purchases', 'kitbuilder_templates', 'public_kitbuilder_templates', 'samples_purchased', 'templates_followed', "template_follows")
        read_only_fields = ('last_4_digits', 'stripe_id')


class UserProfilePublicSerializer(serializers.ModelSerializer):
    # public_kitbuilder_templates = KitBuilderTemplateSerializer(many=True, read_only=True)
    # Need username available here because the useraccount will not be available when the public serializer is in use.
    username = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'image', 'created_at', 'updated_at', 'public_kitbuilder_templates', 'templates_followed')
        read_only_fields = ('id', 'username', 'image', 'created_at', 'updated_at', 'public_kitbuilder_templates', 'templates_followed', "template_follows")