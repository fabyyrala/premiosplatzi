from django.urls import path

from . import views #de polls importa el archivo de views


app_name = "polls"
urlpatterns = [
    #<int:> significa que va a recibir un entero, es la manera que tiene django de saber que es una variable
    
    #ejemplo: /polls/
    path('', views.IndexView.as_view(), name='index'), #view.index trae a la funcion index que esta dentro de views.py(esa funcion tiene hello world)
    
    #ejemplo: /polls/5 esto es para acceder a la pregunta con el id 5 y sus detalles
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    
    #ejemplo: /polls/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    
    #ejemplo: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

]
