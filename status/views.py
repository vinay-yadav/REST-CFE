from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from status.api.serializers import StatusSerializer
from .models import Status


class StatusListSearchAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        qs = Status.object.all()
        serializer = StatusSerializer(qs, many=True)
        return Response(serializer.data)


class StatusAPIView(generics.ListAPIView):
    # queryset = Status.object.all()
    serializer_class = StatusSerializer

    def get_queryset(self):
        qs = Status.object.all()
        query = self.request.GET.get('q', None)

        if query:
            qs = qs.filter(content__icontains=query)

        return qs


class StatusCreateAPIView(generics.CreateAPIView):
    queryset = Status.object.all()
    serializer_class = StatusSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StatusDetailsAPIView(generics.RetrieveAPIView):
    queryset = Status.object.all()
    serializer_class = StatusSerializer

    # lookup_field = 'id'

    # either get_object method or lookup_field
    def get_object(self, *args, **kwargs):
        return Status.object.get(pk=self.kwargs.get('id'))


class StatusUpdateAPIView(generics.UpdateAPIView):
    queryset = Status.object.all()
    serializer_class = StatusSerializer
    lookup_field = 'id'


class StatusDeleteAPIView(generics.DestroyAPIView):
    queryset = Status.object.all()
    serializer_class = StatusSerializer
    lookup_field = 'id'
