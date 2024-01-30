from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TarefaSerializer, UserSerializer
from base.models import Tarefa
from .forms import CriarTarefaForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout

#AUTHENTICATION (START)

@api_view(['GET'])
def getAllUsers(request):
    if request.user.is_authenticated:
        users = User.objects.all()
        if users.count() == 0:
            return Response({'Message':"Nenhum usuário cadastrado!"})
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    else:
        return Response({"Message":"Você precisa estar logado para ter acesso a essa página!"})

@api_view(['POST'])
def createUser(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        userExists = User.objects.get(username=username)
    except:
        userExists = None

    if username == None or email == None or password == None:
        return Response({"Message":"Informações incorretas!"})
    elif userExists:
        return Response({"Message":"Usuário já cadastrado!"})

    user = User.objects.create(username=username, email=email, password=make_password(password))

    if user:
        return Response({"Message":"Usuário Criado!"})
    else:
        return Response({"Message":"Erro"})
    
@api_view(["POST"])
def userLogin(request):
    username = request.data.get("username")
    password = request.data.get("password")

    try:
        user = User.objects.get(username=username)
        print(user) 
    except:
        return Response({"Message":"Não encontrado!"})

    if user.check_password(password):
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({"Message":"Logado com sucesso!"})
    else:
        return Response({"Message":"Informações Incorretas!"})

@api_view(["GET"])
def userLogout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        return Response({"Message":"Usuário deslogado!"})
    else:
        return Response({"Message":"Não existe nenhum usuário deslogado!"})

@api_view(['GET'])
def checkLogin(request):
    user = request.user
    if user.is_authenticated:
        return Response({"Message":"Usuário Logado", "Username":user.username})
    else:
        return Response({"Message":"Nenhum Usuário Logado!"})

#AUTHENTICATION (ENDS)

@api_view(['GET'])
def getData(request):
    if request.user.is_authenticated:
        tarefa = Tarefa.objects.filter(user=request.user)
        serializer = TarefaSerializer(tarefa, many=True)
        return Response(serializer.data)
    else:
        return Response({"message":"Usuário necessita estar logado!"})

@api_view(['POST'])
def addtarefa(request):
    if request.user.is_authenticated:        
        forms = CriarTarefaForm(data=request.data)
        if forms.is_valid():
            task = forms.save(commit=False)
            task.user = request.user
            task.save()

        return Response(forms.data)
    else:
        return Response({"message":"Usuário necessita estar logado!"})


@api_view(['DELETE'])
def delete_tarefa(request, pk):
    if request.user.is_authenticated:
        id = pk
        try:
            tarefa = Tarefa.objects.get(id=id)
        except Tarefa.DoesNotExist:
            return Response({"message": "Tarefa não encontrada"})
        
        if tarefa.user == request.user:
            tarefa.delete()
            return Response({"message":"Essa tarefa foi deletada com sucesso!"})
        else:
            return Response({"message":"Essa tarefa não pertence a você!"})
    else:
        return Response({"message":"Usuário necessita estar logado!"})

@api_view(['PUT'])
def update_tarefa(request):
    if request.user.is_authenticated:
        id = request.data.get("id")
        try:
            tarefa = Tarefa.objects.get(id=id)
        except Tarefa.DoesNotExist:
            return Response({"message": "Tarefa não encontrada"})
        if tarefa.user == request.user:
            forms = CriarTarefaForm(instance=tarefa, data=request.data)
            if forms.is_valid():
                forms.save()
                return Response({"message": "Tarefa atualizada com sucesso"})
            return Response(forms.errors)
        else:
            return Response({"message":"Essa tarefa não te pertence!"})
    else:
        return Response({"message":"Usuário necessita estar logado!"})
    