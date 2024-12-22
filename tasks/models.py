from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True) #se añade por defecto, por lo que para verlo en el panel admin debo generar una logica en el admin.py
    datecompleted = models.DateTimeField(null=True,blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #just because we used the default model User from Django
    def __str__(self): 
        return self.title + ' - ' + self.user.username
    

# null=True
# Indica que este campo puede almacenar valores nulos (NULL) en la base de datos. Esto significa que no es obligatorio que este campo tenga un valor en la base de datos.

# blank=True
# Define que este campo puede dejarse vacío en los formularios de Django (a nivel del formulario, no necesariamente en la base de datos). Si no se incluye blank=True, Django obligará a llenar este campo en formularios.