from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Book
from .serializers import BookSerializer


class BookPagination(PageNumberPagination):
    """
    Custom pagination class to control page size.
    Default is 10, but client can override it using ?page_size=...
    Maximum allowed page size is 20.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Book objects.
    Provides list, create, retrieve, update, and delete operations.
    Supports filtering by author, published_date, and language using django-filter.
    """
    queryset = Book.objects.all().order_by("-id")
    serializer_class = BookSerializer
    pagination_class = BookPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'published_date', 'language']
