from rest_framework import viewsets
from .models import Produtos 
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import Produto_Serializer
from django.shortcuts import render, get_object_or_404 

class ProdutoView(viewsets.ModelViewSet):
    queryset = Produtos.objects.all()
    serializer_class = Produto_Serializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['certificado']
    search_fields = ['nome', 'descricao']
    
    def perform_create(self, serializer):
       
        serializer.save(dono=self.request.user)
        
def produto_publico(request, pk):
    
    produto = get_object_or_404(Produtos, pk=pk)
    
    
    return render(request, 'products/detalhe_produto.html', {'produto': produto})