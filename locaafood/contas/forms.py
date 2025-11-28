from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class CadastroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'tipo_usuario', 'nome_companhia']
        
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo_usuario')
        companhia = cleaned_data.get('nome_companhia')

        # Validação: Se for Empresa, obriga a ter nome da companhia
        if tipo == 'EMPRESA' and not companhia:
            self.add_error('nome_companhia', 'Empresas devem informar o Nome da Companhia.')
        
        return cleaned_data

class LoginUsuarioForm(AuthenticationForm):
    pass