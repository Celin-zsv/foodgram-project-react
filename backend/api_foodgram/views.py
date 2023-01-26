from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from.serializers import TagSerializer
from .models import Tag


def zsv_page(request):
    return HttpResponse('ЭТО zsv page!')


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
