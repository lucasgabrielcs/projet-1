from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# Função que joga o usuário para o login quando acessa a home
def redirecionar_para_login(request):
    return redirect('login') 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Suas rotas de API/Produtos
    path('api/', include('products.urls')),
    
    # Rotas de Autenticação (Login/Cadastro)
    # Importante: O nome 'contas.urls' deve existir (criamos ele nos passos anteriores)
    path('auth/', include('contas.urls')), 

    # Rota da Página Inicial (Vazia) -> Redireciona para Login
    path('', redirecionar_para_login),
]

# Configuração para servir imagens (QR Codes e PDFs)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)