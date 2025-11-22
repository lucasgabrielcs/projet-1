from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Produtos
from .serializers import Produto_Serializer
from .forms import ProdutoForm

# === 1. API (O Motor para JSON e Apps) ===
class ProdutoView(viewsets.ModelViewSet):
    queryset = Produtos.objects.all()
    serializer_class = Produto_Serializer
    
    # Configuração dos Filtros da API
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['certificado']
    search_fields = ['nome', 'descricao']

    def perform_create(self, serializer):
        # Define o dono automaticamente se estiver logado
        # (Se for AnonymousUser, vai dar erro na API, mas no Dashboard tratamos abaixo)
        if self.request.user.is_authenticated:
            serializer.save(dono=self.request.user)
        else:
            serializer.save()

# === 2. PAGINA PÚBLICA (Destino do QR Code) ===
def produto_publico(request, pk):
    produto = get_object_or_404(Produtos, pk=pk)
    return render(request, 'products/detalhe_produto.html', {'produto': produto})

# === 3. DASHBOARD (Gestão Completa) ===

# LISTA + CRIAR NOVO (Tudo na mesma tela)
def lista_produtos(request):
    produtos = Produtos.objects.all()
    form = ProdutoForm() # Formulário vazio para o modal

    if request.method == "POST":
        # Se clicou em "Salvar" no modal de novo produto
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto_novo = form.save(commit=False)
            
            # Truque para garantir um dono mesmo sem login (apenas para seu teste funcionar)
            # Em produção, isso seria obrigatório ser o request.user
            if request.user.is_authenticated:
                produto_novo.dono = request.user
            else:
                # Pega o primeiro usuário do banco (admin) "emprestado" para não dar erro
                from django.contrib.auth import get_user_model
                User = get_user_model()
                produto_novo.dono = User.objects.first() 
            
            produto_novo.save()
            return redirect('lista_produtos') # Recarrega a página limpa

    return render(request, 'products/lista_produtos.html', {
        'produtos': produtos,
        'form': form
    })

# EDITAR (Processa o modal de edição e volta)
def editar_produto(request, pk):
    produto = get_object_or_404(Produtos, pk=pk)
    
    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
    
    return redirect('lista_produtos')

# EXCLUIR (Processa o modal de exclusão e volta)
def excluir_produto(request, pk):
    produto = get_object_or_404(Produtos, pk=pk)
    
    if request.method == "POST":
        produto.delete()
    
    return redirect('lista_produtos')