from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CadastroUsuarioForm, LoginUsuarioForm

def cadastro(request):
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('lista_produtos') # Garanta que essa rota existe
    else:
        form = CadastroUsuarioForm()
    return render(request, 'contas/cadastro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginUsuarioForm(data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('lista_produtos')
    else:
        form = LoginUsuarioForm()
    return render(request, 'contas/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')