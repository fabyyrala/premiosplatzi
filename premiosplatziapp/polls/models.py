import datetime

from django.db import models
from django.utils import timezone
# Create your models here.

class Question(models.Model):
   question_text = models.CharField(max_length=200) #Charfield va a equivar a un string
   pub_date = models.DateTimeField('date published')
   
   def __str__(self):
       return self.question_text
   
   def was_published_recently(self):
       #Nos dice si la fecha de publicacion es mayor a la fecha actual , puede tener un dia como maximo de actualizacion
       return self.pub_date >= timezone.now() - datetime.timedelta(days=1) #Timedelta es un objeto que nos define una diferencia de tiempo
       




class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)#Foreing key conecta choices con question
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)#con default 0 le defino que va a ser un contador
    
    def __str__(self):
       return self.choice_text