from tkinter import CASCADE
from django.db import models

# Una vez que hayamos decidido cuáles serán nuestros modelos y sus campos, debemos pensar en la relación que existe entre ellos. Django le permite definir relaciones de uno a uno 
# (OneToOneField), de uno a muchos (ForeignKey) y de muchos a muchos (ManyToManyField).
class Usuario(models.Model):
    nombre= models.CharField("nombre", max_length=100)
    apellido=models.CharField("apellido", max_length=100)
    email= models.EmailField()
    temas_favoritos= models.CharField("temasFav", max_length=100)

class Tematica(models.Model):
    nombre=models.CharField(max_length=100)

class Lenguaje(models.Model):
    nombreLenguaje=models.CharField(max_length=50)

class Post(models.Model):
    posteador= models.ForeignKey(Usuario,on_delete=models.CASCADE)
    #foreingKey porque un Post tiene un solo posteador/usuario pero cada
    #usuario puede tener muchos posts
    titulo= models.CharField(max_length=100)
    contenido= models.TextField()
    fecha_publicacion=models.DateTimeField(auto_now_add=True)
    actualizacion=models.DateTimeField(auto_now=True)
    tipoPost=models.CharField(max_length=50)
    tematica= models.ManyToManyField(Tematica)
    #mantyToManyField porque un post puede abarcar distintas tematicas

class Likes(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)

class ComentariosPost(models.Model):
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    #foreignKey porque un comentario está en un SOLO post pero cada Post puede tener
    #muchos comentarios
    fecha= models.DateTimeField(auto_now_add=True)
    contenido_comentario=models.TextField()
    comentarista= models.ForeignKey(Usuario,on_delete=models.CASCADE)
    #ForeignKey porque un comentario tiene un solo comentarista pero 
    #cada usuario puede hacer muchos comentarios

class VistaDelPost(models.Model):
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    visto= models.DateTimeField(auto_now_add=True)