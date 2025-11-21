from rest_framework import serializers
from .models import Produtos

class Produto_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Produtos
        
        fields = ["id","nome","descricao", "certificado","qr_code"]