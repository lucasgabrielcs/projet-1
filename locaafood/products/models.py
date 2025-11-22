from django.db import models
from django.conf import settings
import qrcode
import json  # <--- 1. Importamos a biblioteca JSON
from io import BytesIO
from django.core.files import File

class Produtos(models.Model):
    nome = models.CharField(max_length=255)
    certificado = models.BooleanField(default=False)
    dono = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    descricao = models.TextField()
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)

    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        # 1. Salvamos primeiro para garantir que o produto tem um ID (pk)
        if not self.pk:
            super().save(*args, **kwargs)

        # 2. Criamos o Dicionário (O pacote de dados)
        # Convertemos os dados do banco para um formato que o Python entende (dict)
        dados_produto = {
            "id": self.pk,
            "nome": self.nome,
            "descricao": self.descricao,
            "certificado": self.certificado,
            # Atenção: Pegamos o .username (texto), pois o JSON não lê objetos inteiros
            "dono": self.dono.username if self.dono else "Desconhecido"
        }

        # 3. Transformamos em Texto JSON (A String Mágica)
        # indent=4: Deixa bonitinho e legível
        # ensure_ascii=False: Permite acentos (ex: "café" em vez de "caf\u00e9")
        json_string = json.dumps(dados_produto, indent=4, ensure_ascii=False)
        
        # 4. Geramos o QRCode com esse TEXTO JSON
        imagem_qr = qrcode.make(json_string)
        
        # 5. Preparamos a memória e salvamos
        buffer = BytesIO()
        imagem_qr.save(buffer)
        buffer.seek(0)

        # 6. Salvamos a imagem no campo do banco
        # save=False é vital para evitar loop infinito
        self.qr_code.save(f'{self.nome}_json_{self.pk}.png', File(buffer), save=False)

        # 7. Salvamento final no banco
        super().save(*args, **kwargs)