from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, generics, pagination
from rest_framework_jwt.settings import api_settings
from status.models import Status
from status.views import StatusAPIView
from .serializers import UserRegisterSerializer, UserDetailSerializer, StatusInlineSerializer
from .permissions import AnonPermissionOnly

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'username'

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}


class UserStatusAPIView(StatusAPIView):
    serializer_class = StatusInlineSerializer

    def get_queryset(self, *args, **kwargs):
        return Status.object.filter(user__username=self.kwargs.get('username')).order_by('-timestamp')

    def post(self, request, *args, **kwargs):
        return Response({'details': 'Method not allowed'}, status=400)


# class UserStatusAPIView(generics.ListAPIView):
#     serializer_class = StatusInlineSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def get_queryset(self, *args, **kwargs):
#         return Status.object.filter(user__username=self.kwargs.get('username')).order_by('-timestamp')


class AuthAPIView(APIView):
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


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AnonPermissionOnly]

    # to pass extra data to the serializer
    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}

# class RegisterAPIView(APIView):
#     permission_classes = [permissions.AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return Response({'msg': 'you are already registered and authenticated'}, status=400)
#
#         data = request.data
#         print(data)
#         username = data.get('username', None)
#         email = data.get('email', None)
#         password = data.get('password', None)
#         password2 = data.get('password2', None)
#
#         qs = User.objects.filter(
#             Q(username__iexact=username) |
#             Q(email__iexact=username)
#         )
#
#         if not qs.exists():
#             if password2 != password:
#                 return Response('Password must match.', status=401)
#
#             user = User.objects.create(username=username, email=email)
#             user.set_password(password)
#             user.save()
#
#             payload = jwt_payload_handler(user)
#             token = jwt_encode_handler(payload)
#             response = jwt_response_payload_handler(token, user)
#
#             return Response(response)
#
#         return Response('This user already exists', status=401)
