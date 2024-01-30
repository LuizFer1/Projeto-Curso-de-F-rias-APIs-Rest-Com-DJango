from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TarefaSerializer
from base.models import Tarefa
from .forms import CriarTarefaForm

@api_view(['GET'])
def getData(request):
    tarefa = Tarefa.objects.all()
    serializer = TarefaSerializer(tarefa, many=True)
    return Response(serializer.data)
@api_view(['POST'])
def addtarefa(request):
    forms = CriarTarefaForm(data=request.data)
    if forms.is_valid():
        forms.save()
    return Response(forms.data)
@api_view(['DELETE'])
def delete_tarefa(request):
    id = request.data.get("id")
    
    try:
        tarefa = Tarefa.objects.get(id=id)
    except Tarefa.DoesNotExist:
        return Response({"message": "Tarefa não encontrada"})
    
    return Tarefa.delete()

@api_view(['PUT'])
def update_tarefa(request):
    id = request.data.get("id")

    try:
        tarefa = Tarefa.objects.get(id=id)
    except Tarefa.DoesNotExist:
        return Response({"message": "Tarefa não encontrada"})
    forms = CriarTarefaForm(instance=tarefa, data=request.data)
    if forms.is_valid():
        forms.save()
        return Response({"message": "Tarefa atualizada com sucesso"})
    return Response(forms.errors)
