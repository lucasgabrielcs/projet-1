from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Produtos
from .serializers import Produto_Serializer
from .forms import ProdutoForm

class ProdutoView(viewsets.ModelViewSet):
    queryset = Produtos.objects.all()
    serializer_class = Produto_Serializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['certificado']
    search_fields = ['nome', 'descricao']

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(dono=self.request.user)
        else:
            serializer.save()

def produto_publico(request, pk):
    produto = get_object_or_404(Produtos, pk=pk)
    return render(request, 'products/detalhe_produto.html', {'produto': produto})


# ... dentro de products/views.py ...

def lista_produtos(request):
    produtos = Produtos.objects.all()
    form = ProdutoForm()

    if request.method == "POST":
        # === AQUI ESTAVA O ERRO ===
        # Antes estava: form = ProdutoForm(request.POST)
        # TEM QUE SER ASSIM:
        form = ProdutoForm(request.POST, request.FILES) # <--- ADICIONE O request.FILES
        
        if form.is_valid():
            produto_novo = form.save(commit=False)
            
            if request.user.is_authenticated:
                produto_novo.dono = request.user
            else:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                produto_novo.dono = User.objects.first() 
            
            produto_novo.save()
            return redirect('lista_produtos')

    return render(request, 'products/lista_produtos.html', {
        'produtos': produtos,
        'form': form
    })


def editar_produto(request, pk):
    produto = get_object_or_404(Produtos, pk=pk)
    
    if request.method == "POST":
        # Adicione request.FILES aqui também!
        form = ProdutoForm(request.POST, request.FILES, instance=produto) # <--- AQUI
        if form.is_valid():
            form.save()
    
    return redirect('lista_produtos')

# EXCLUIR (Processa o modal de exclusão e volta)
def excluir_produto(request, pk):
    produto = get_object_or_404(Produtos, pk=pk)
    
    if request.method == "POST":
        produto.delete()
    
    return redirect('lista_produtos')