from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutoView

router = DefaultRouter()
router.register(r'produtos',ProdutoView)

urlpatterns = [
    path('' , include(router.urls)),
]
    