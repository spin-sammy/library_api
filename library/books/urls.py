from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

# Create a router and register the BookViewSet with it
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

# Include the router URLs in the urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]