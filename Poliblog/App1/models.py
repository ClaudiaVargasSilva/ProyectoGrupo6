from django.db import models

class Usuarios(models.Model):
    nombre= models.CharField("nombre", max_length=100)
    apellido= models.CharField("apellido", max_length=100)
    email= models.EmailField()
    #contrasena=models.cont
