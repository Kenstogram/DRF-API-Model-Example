from django.urls import path, include

from rest_framework.routers import DefaultRouter
from core import views
from rest_framework.schemas import get_schema_view

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'tables', views.TableViewSet)
router.register(r'users', views.UserViewSet)

schema_view = get_schema_view(title='Pastebin API')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('schema/', schema_view),
    path('', include(router.urls)),
]
