from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from apps.docs.models import Document
from apps.docs.serializers import DocumentSerializer


class DocumentView(ModelViewSet):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['title']
