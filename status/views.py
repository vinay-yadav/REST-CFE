from django.shortcuts import get_object_or_404
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from status.api.serializers import StatusSerializer
from accounts.permissions import IsOwnerOrReadOnly
from .models import Status


class StatusAPIView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.ListAPIView
):
    search_fields = ['user__username', 'content']
    ordering_fields = ['user__username', 'timestamp']

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [TokenAuthentication]                  # default = SessionAuthentication
    serializer_class = StatusSerializer
    queryset = Status.object.all()

    # lookup_field = 'id'

    # commented as 'search_fields' is doing the same
    # def get_queryset(self):
    #     qs = Status.object.all()
    #     query = self.request.GET.get('q', None)
    #     if query:
    #         qs = qs.filter(content__icontains=query)
    #     return qs.order_by('-timestamp')

    def get_object(self):
        request = self.request
        passed_id = request.GET.get('id', None)
        queryset = self.get_queryset()
        obj = None
        if passed_id is not None:
            obj = get_object_or_404(queryset, id=passed_id)
            self.check_object_permissions(request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        passed_id = request.GET.get('id', None)
        if passed_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class StatusAPIView(generics.ListCreateAPIView):
#     serializer_class = StatusSerializer
#
#     def get_queryset(self):
#         qs = Status.object.all()
#         query = self.request.GET.get('q', None)
#         if query:
#             qs = qs.filter(content__icontains=query)
#         return qs


class StatusDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.object.all()
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = 'id'

# class StatusListSearchAPIView(APIView):
#     permission_classes = []
#     authentication_classes = []
#
#     def get(self, request):
#         qs = Status.object.all()
#         serializer = StatusSerializer(qs, many=True)
#         return Response(serializer.data)


# CreateModelMixin ---> POST
# class StatusAPIView(mixins.CreateModelMixin, generics.ListAPIView):
#     # queryset = Status.object.all()
#     serializer_class = StatusSerializer
#
#     def get_queryset(self):
#         qs = Status.object.all()
#         query = self.request.GET.get('q', None)
#         if query:
#             qs = qs.filter(content__icontains=query)
#         return qs
#
#     # Comes with CreateModelMixin
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class StatusCreateAPIView(generics.CreateAPIView):
#     queryset = Status.object.all()
#     serializer_class = StatusSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# UpdateModelMixin ---> PUT
# DestroyModelMixin --> DELETE
# class StatusDetailsAPIView(mixins.DestroyModelMixin, mixins.UpdateModelMixin, generics.RetrieveAPIView):
#     # queryset = Status.object.all()
#     serializer_class = StatusSerializer
#     # lookup_field = 'id'
#
#     # use either get_object method and specify keyword or lookup_field
#     def get_object(self, *args, **kwargs):
#         return Status.object.get(pk=self.kwargs.get('id'))
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def patch(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# class StatusUpdateAPIView(generics.UpdateAPIView):
#     queryset = Status.object.all()
#     serializer_class = StatusSerializer
#     lookup_field = 'id'
#
#
# class StatusDeleteAPIView(generics.DestroyAPIView):
#     queryset = Status.object.all()
#     serializer_class = StatusSerializer
#     lookup_field = 'id'
