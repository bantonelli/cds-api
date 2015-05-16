from rest_framework import serializers
from userprofile.models import UserProfile
from api.api_v1.kitbuilder.serializers import KitBuilderPurchaseSerializer, KitBuilderTemplateSerializer


#-------------------------------------------------------------->
# USER PROFILE
class UserProfilePrivateSerializer(serializers.ModelSerializer):
    # Needs Object level permission
    kitbuilder_purchases = KitBuilderPurchaseSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('kitbuilder_templates', instance.kitbuilder_templates)
        instance.public = validated_data.get('templates_followed', instance.templates_followed)
        instance.save()
        return instance

    class Meta:
        model = UserProfile
        fields = ('id', 'last_4_digits', 'stripe_id', 'created_at', 'updated_at', 'kitbuilder_purchases', 'kitbuilder_templates', 'samples_purchased', 'templates_followed')
        read_only_fields = ('last_4_digits', 'stripe_id')


class UserProfilePublicSerializer(serializers.ModelSerializer):
    public_kitbuilder_templates = KitBuilderTemplateSerializer(many=True, read_only=True)
    # Need username available here because the useraccount will not be available when the public serializer is in use.
    username = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'created_at', 'updated_at', 'public_kitbuilder_templates')