from django.shortcuts import render
from .models import Tarefa, Usuario
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def formlogin(request):

    if request.method == "POST":
        usuario = request.POST['login']
        senha = request.POST['senha']        
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/tarefas/listartarefas")
    
    return render(request, "login.html")

def logout_view(request):
    logout(request)

    return HttpResponseRedirect("/tarefas/login")

@login_required(login_url="/tarefas/login")
def listarTarefas(request):

    if request.method == "GET" and request.GET.get('busca'):
        tarefas = Tarefa.objects.filter(titulo__icontains=request.GET.get('busca'))
    else:
        tarefas = Tarefa.objects.all()

    return render(request, "listarTarefas.html", {"tarefas" : tarefas})

@login_required(login_url="/tarefas/login")
def listarUsuarios(request):

    usuarios = Usuario.objects.all()

    return render(request, "listarUsuarios.html", {"usuarios": usuarios})

@login_required(login_url="/tarefas/login")
def cadastroAtividade(request):

    if(request.method == "POST"):
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')        
        ano = int(request.POST.get('data').split("-")[0])
        mes = int(request.POST.get('data').split("-")[1])
        dia = int(request.POST.get('data').split("-")[2])
        data = datetime(ano, mes, dia)
        usuario = Usuario.objects.get(id=request.POST.get('usuario'))

        nova_atividade = Tarefa(titulo=titulo, 
                                descricao=descricao, 
                                data=data, 
                                usuario=usuario)
        nova_atividade.save()

        return HttpResponseRedirect('/tarefas/listartarefas')

    usuarios = Usuario.objects.all()

    return render(request, "cadastroAtividade.html", {'usuarios':usuarios})

@login_required(login_url="/tarefas/login")
def cadastroUsuario(request):
    return render(request, "cadastroUsuario.html")

@login_required(login_url="/tarefas/login")
def excluirAtividade(request, id):

    tarefa = Tarefa.objects.get(id=id)
    tarefa.delete()

    return HttpResponseRedirect('/tarefas/listartarefas')

@login_required(login_url="/tarefas/login")
def editarAtividade(request, id):

    if request.method == "POST":
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')        
        ano = int(request.POST.get('data').split("-")[0])
        mes = int(request.POST.get('data').split("-")[1])
        dia = int(request.POST.get('data').split("-")[2])
        data = datetime(ano, mes, dia)
        usuario = Usuario.objects.get(id=request.POST.get('usuario'))

        editar_atividade = Tarefa.objects.get(id=id)
        editar_atividade.titulo = titulo
        editar_atividade.descricao = descricao
        editar_atividade.data = data
        editar_atividade.usuario = usuario
        editar_atividade.save()

        return HttpResponseRedirect('/tarefas/listartarefas')
    else:
        tarefa = Tarefa.objects.get(id=id)
        usuarios = Usuario.objects.all()

    return render(request, "editarAtividade.html",{'tarefa': tarefa, 'usuarios':usuarios})