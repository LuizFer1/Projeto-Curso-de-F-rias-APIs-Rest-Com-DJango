from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('add/',views.addtarefa),
    path('dell/<str:pk>/',views.delete_tarefa),
    path('update/',views.update_tarefa),
    path('users/', views.getAllUsers), 
    path('createUser/', views.createUser),
    path('checkLogin/', views.checkLogin),
    path('login/', views.userLogin),
    path('logout/', views.userLogout)
]
