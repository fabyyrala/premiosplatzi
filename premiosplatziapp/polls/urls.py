from django.urls import path
from . import views #de polls importa el archivo de views

urlpatterns = [
    path('', views.index, name='index'), #view.index trae a la funcion index que esta dentro de views.py(esa funcion tiene hello world)
]