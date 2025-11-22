from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutoView
from .views import ProdutoView, produto_publico, lista_produtos

router = DefaultRouter()
router.register(r'produtos',ProdutoView)

urlpatterns = [
    path('' , include(router.urls)),
    path('produto/<int:pk>/visualizar/', produto_publico, name='produto_publico'),
    path('catalogo/', lista_produtos, name='lista_produtos'),
]

    