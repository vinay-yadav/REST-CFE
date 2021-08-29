import datetime
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model
from status.models import Status
from rest_framework_jwt.settings import api_settings

expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()


class StatusInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = [
            'content',
            'image',
            'timestamp'

        ]


class UserDetailSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'status'
        ]

    def get_status(self, obj):
        request = self.context.get('request')
        limit = 10

        if request.GET.get('limit', None):
            limit = int(request.GET.get('limit'))

        qs = obj.status_set.all()[:limit]
        return StatusInlineSerializer(qs, many=True).data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    # token = serializers.SerializerMethodField(read_only=True)
    # expiration_date = serializers.SerializerMethodField(read_only=True)
    token_response = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        # fields = '__all__'
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2',
            # 'token',
            # 'expiration_date',
            'token_response'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    # def validate_username(self, value):
    #     if User.objects.filter(username__iexact=value).exists():
    #         raise serializers.ValidationError('Username already exists')
    #     return value

    def validate(self, data):
        password = data.get('password', None)
        password2 = data.pop('password2', None)

        if password2 != password:
            raise serializers.ValidationError('Passwords must match')
        return data

    # def get_expiration_date(self, obj):
    #     return timezone.now() + expire_delta - datetime.timedelta(seconds=200)
    #
    # def get_token(self, obj):
    #     payload = jwt_payload_handler(obj)
    #     token = jwt_encode_handler(payload)
    #     return token

    def get_token_response(self, obj):
        print('serializer context', self.context)  # can access request now
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return jwt_response_payload_handler(token, obj)

    def create(self, validated_data):
        user_obj = User(username=validated_data.get('username'), email=validated_data.get('email'))
        user_obj.first_name = validated_data.get('first_name')
        user_obj.last_name = validated_data.get('last_name')
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()

        return user_obj
