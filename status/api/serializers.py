from rest_framework import serializers
from status.models import Status
from accounts.serializers import UserSerializer


class StatusSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Status
        fields = '__all__'
        read_only_fields = ['user']
        # depth = 1

    def validate_content(self, value):
        if len(value) > 249:
            raise serializers.ValidationError('Content too long!!')
        return value

    def validate(self, data):
        content = data.get('content', None)
        if content == '':
            content = None
        image = data.get('image', None)

        if content is None and image is None:
            raise serializers.ValidationError('Either content or image is required!!')
        return data


class CustomSerializer(serializers.Serializer):
    """Only difference between Serializer and ModalSerializer is Serializers does not have save()"""
    content = serializers.CharField()
    email = serializers.EmailField()
