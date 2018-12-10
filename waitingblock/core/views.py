from core.models import Table
from django.contrib.auth.models import User
from core.serializers import TableSerializer
from core.serializers import UserSerializer
from rest_framework import generics
from rest_framework import permissions
from core.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers

from django.db import models
from django_tables2 import MultiTableMixin, RequestConfig
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from django.contrib.auth.forms import UserCreationForm
from django.views import generic

from .models import Table


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TableViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        table = self.get_object()
        return Response(table.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'tables': reverse('tables-list', request=request, format=format)
    })

class IndexView(TemplateView):
    model = Table
    template_name = 'waitingblock/index.html'
    context_object_name = 'table'

    def form_valid(self, form):
        form.save()
        return redirect('home')

    def redirect_view(request):
        response = redirect('home')
        return response

"""
class TableList(generics.ListCreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TableDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly,)

class TableHighlight(generics.GenericAPIView):
    queryset = Table.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        table = self.get_object()
        return Response(table.highlighted)
"""
