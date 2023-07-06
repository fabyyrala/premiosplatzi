from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404 #get_object_or_404 es una función que nos permite obtener un objeto de un modelo en particular o en caso de que no exista, nos devuelve un error 404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic


from .models import Question, Choice

# def index(request):
#     lastest_question_list = Question.objects.all()#con esto tengo un objeto tipo query donde se guardaron todas las preguntas
#     return render(request,"polls/index.html",{
#         "latest_question_list":lastest_question_list
#         })#con esto renderizo la pagina,render es una función que toma como primer argumento el objeto request, un template y un diccionario opcional con variables que se usarán en el template. Devuelve un objeto HttpResponse con el contenido del template renderizado.

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)# primer argumento es el modelo a partir del cual vamos a buscar, el segundo es el valor a partir del cual vamos a buscar internamente en el modelo, en este caso el id de la pregunta
#     return render(request, "polls/detail.html",{
#         "question":question
#     })


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html",{
#         "question":question
#     })
 
 
#-------------------VISTAS BASADAS EN CLASES----------------
   
class IndexView(generic.ListView):
    template_name="polls/index.html"  ##especifica el template que va a usar la vista
    context_object_name = "latest_question_list"##especifica el nombre de la variable que va a contener la lista de objetos que se van a mostrar en el template
    
    def get_queryset(self): ##sobreescribe el método get_queryset para que devuelva las últimas 5 preguntas
        '''Return the last five published questions.'''
        return Question.objects.order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    
     
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html" 
    
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])# request.POST es un diccionario que nos permite acceder a los datos enviados por el usuario a través de un formulario, CHOICE es el nombre que viene de "name" en el template. 
        ## esta dentro de TRY porque si no existe el valor de CHOICE, se va a ejecutar el EXCEPT.
        
    except(KeyError,Choice.DoesNotExist): #KeyError es el error que se genera cuando no se encuentra una llave en un diccionario
        return render(request, "polls/detail.html",{
            "question":question,
            "error_message": "No elegiste una respuesta"   
        })
    else: ##else se ejecuta si no hay error
        selected_choice.votes += 1 #accede al valor de votes y le suma 1
        selected_choice.save() #guarda el valor de votes en la base de datos
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))