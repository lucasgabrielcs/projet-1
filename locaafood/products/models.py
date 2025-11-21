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
    
    def save(self, *args , **kwargs ):
        imagem_qr = qrcode.make(self.nome)
        buffer = BytesIO()
        imagem_qr.save(buffer)
        buffer.seek(0)
        if not self.qr_code:
            self.qr_code.save(f'{self.nome}.png', File(buffer), save=False)
        super().save(*args, **kwargs)
        
        