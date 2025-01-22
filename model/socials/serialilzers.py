from rest_framework import serializers

class SocialAccountSerializer(serializers.Serializer):
    decision = serializers.ChoiceField(choices=['link', 'create_new'])
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    provider = serializers.CharField()
    social_id = serializers.CharField()