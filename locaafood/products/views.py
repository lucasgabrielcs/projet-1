from rest_framework import viewsets
from .models import Produtos 
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import Produto_Serializer

class ProdutoView(viewsets.ModelViewSet):
    queryset = Produtos.objects.all()
    serializer_class = Produto_Serializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['certificado']
    search_fields = ['nome', 'descricao']
    
    def perform_create(self, serializer):
       
        serializer.save(dono=self.request.user)