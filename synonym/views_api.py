from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from synonym.models import Word
from .serializers import WordModelSerializer


class WordApiViewSet(ModelViewSet):

    queryset = Word.objects.all()
    serializer_class = WordModelSerializer


