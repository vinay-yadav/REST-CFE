from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from status.api.serializers import StatusSerializer
from .models import Status


class StatusAPIView(generics.ListCreateAPIView):
    serializer_class = StatusSerializer

    def get_queryset(self):
        qs = Status.object.all()
        query = self.request.GET.get('q', None)
        if query:
            qs = qs.filter(content__icontains=query)
        return qs


class StatusDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.object.all()
    serializer_class = StatusSerializer
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
