from rest_framework import pagination


class CustomPagination(pagination.LimitOffsetPagination):
    default_limit = 5
    max_limit = 15

# class CustomPagination(pagination.PageNumberPagination):
#     page_size = 5
