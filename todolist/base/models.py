from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tarefa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    titulo = models.CharField(max_length=200)
    descrição = models.TextField()
    concluida = models.BooleanField(default=False)
    