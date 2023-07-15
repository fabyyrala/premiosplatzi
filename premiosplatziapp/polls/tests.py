import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

from .models import Question

class QuestionModelTests(TestCase):#Test case son test que corresponde a una clase
    
    def test_was_published_recently_with_future_question(self): #testeamos si la fecha de publicacion es mayor a la fecha actual , puede tener un dia como maximo de actualizacion
        """was_published_recently returns False for questions whose pub_date is in the future """#Retorna falso para cada pregunta que se cargue en el futuro(es decir la fecha de publicacion es mayor a la fecha actual)
        
        time = timezone.now() + datetime.timedelta(days=30)#PRegunta de 30 dias futuros desde la fecha actual
        future_question = Question(question_text="Quien es el mejor Course Director de Platzi?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        

def create_question(question_text, days):#creamos una funcion que nos permite crear una pregunta con un texto y un numero de dias
    """
    Create a question with the given `question_text` and published the given 
    number of `days` offset to now (negative for questions published in the past, positive for questions that have yet to be published).
    """   
    
    # Calcula la fecha de publicación sumando el desplazamiento a la hora actual 
    time = timezone.now() + datetime.timedelta(days=days)
    
     # Crea y devuelve el objeto de pregunt
    return Question.objects.create(question_text=question_text, pub_date=time)




class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        
        """if no question exist, an appropiate message is displayed"""
        
        #hago una request, traigo el resultado de la vista index, y lo guardo en response
         # Enviar una solicitud GET a la URL especificada
        response = self.client.get(reverse('polls:index'))
        
        #verifico que el status code sea 200, que es el status code de una respuesta exitosa, si response.status_code es igual a 200 significa que la vista se ejecutó correctamente y es igual a true
         # Verificar que el código de estado de la respuesta sea 200 (OK)
        self.assertEqual(response.status_code, 200)#Afirmo que son iguales con assertEqual
        
        
        #verifico que el mensaje "No hay preguntas disponibles" esté en el response, si está en el response es igual a true
        # Verificar que la respuesta contenga el mensaje "No polls are available."
        self.assertContains(response, "No polls are available.")
        
         #verifico que el contexto de la respuesta sea una lista vacía, si es una lista vacía es igual a true
        # Verificar que la lista latest_question_list en el contexto de la respuesta esté vacía
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        
    def test_future_question(self):
        
        """Question with a pub_date in the future aren't displayed on the index page"""
        
        create_question("Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])
        
    
    
    def test_past_questions(self):
        
        """Question with a pub_date in the past aren't displayed on the index page""" 
        
        question = create_question("Past question", days=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question])
        