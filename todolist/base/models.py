from django.db import models

# Create your models here.

class Tarefa(models.Model):
    titulo = models.CharField(max_length=200)
    descrição = models.TextField()
    concluida = models.BooleanField(default=False)
    