from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('add/',views.addtarefa),
    path('dell/',views.delete_tarefa),
    path('update/',views.update_tarefa),
]
