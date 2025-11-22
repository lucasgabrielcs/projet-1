from django.db import models
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files import File
# Create your models here.

class Produtos(models.Model):
    nome = models.CharField(max_length=255)
    certificado = models.BooleanField(default= False)
    dono = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    descricao = models.TextField()
    qr_code = models.ImageField(upload_to='qrcodes/' , blank=True)

    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

        website_url = f"http://127.0.0.1:8000/api/produto/{self.pk}/visualizar/"
        
        imagem_qr = qrcode.make(website_url)
        buffer = BytesIO()
        imagem_qr.save(buffer)
        buffer.seek(0)

        self.qr_code.save(f'{self.nome}_{self.pk}.png', File(buffer), save=False)

        
        super().save(*args, **kwargs)