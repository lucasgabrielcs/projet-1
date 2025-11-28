from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    TIPOS_USUARIO = (
        ('CLIENTE', 'Cliente Consumidor'),
        ('EMPRESA', 'Empresa Certificadora/Produtora'),
    )
    
    # O campo que estava faltando:
    tipo_usuario = models.CharField(max_length=10, choices=TIPOS_USUARIO, default='CLIENTE')
    
    nome_companhia = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.username