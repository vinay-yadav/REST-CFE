from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()


class AuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'msg': 'you are already authenticated'}, status=400)

        data = request.data
        print(data)
        username = data.get('username', None)
        password = data.get('password', None)

        # user = authenticate(username=username, password=password)
        # print(user)

        qs = User.objects.filter(
            Q(username__iexact=username) |
            Q(email__iexact=username)
        )

        if qs.exists():
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj

                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)

                response = jwt_response_payload_handler(token, user)

                return Response(response)

        return Response('Bad Response', status=401)
