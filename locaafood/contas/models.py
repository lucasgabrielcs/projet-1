from django.db import models
from django.contrib.auth.models import AbstractUser 
# Create your models here.

class Usuario(AbstractUser):
    nome_companhia = models.CharField(max_length=255)
    
    def __str__(self):
        return self.username
