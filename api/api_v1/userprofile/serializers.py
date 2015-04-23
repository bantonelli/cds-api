from rest_framework import serializers
from userprofile.models import UserProfile
from api.api_v1.kitbuilder.serializers import KitBuilderPurchaseSerializer, KitBuilderTemplateSerializer

#-------------------------------------------------------------->
# USER PROFILE
class UserProfilePrivateSerializer(serializers.ModelSerializer):
    # Needs Object level permission
    kitbuilder_purchases = KitBuilderPurchaseSerializer(many=True, read_only=True)
    kitbuilder_templates = KitBuilderTemplateSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'last_4_digits', 'stripe_id', 'created_at', 'updated_at', 'kitbuilder_purchases', 'kitbuilder_templates')


class UserProfilePublicSerializer(serializers.ModelSerializer):
    kitbuilder_templates = KitBuilderTemplateSerializer(many=True, read_only=True)
    # Need username available here because the useraccount will not be available when the public serializer is in use.
    username = serializers.Field()

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'created_at', 'updated_at', 'kitbuilder_templates')