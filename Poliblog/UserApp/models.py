from django.utils import timezone
from tkinter import CASCADE
from django.db import models
from django.conf import Settings,settings
from django.contrib.auth.models import AbstractUser


class Usuario(models.Model):
    nombre= models.CharField("nombre", max_length=100)
    apellido=models.CharField("apellido", max_length=100)
    email= models.EmailField()
    temas_favoritos= models.CharField("temasFav", max_length=100)
    #tematica= models.ManyToManyField("tematicas", max_length=50)





class Tematica(models.Model):
    nombre=models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombre}'

class Lenguaje(models.Model):
    nombreLenguaje=models.CharField(max_length=50)
class Post(models.Model):
    id= models.AutoField(primary_key=True)
    posteador= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    #foreingKey porque un Post tiene un solo posteador/usuario pero cada
    #usuario puede tener muchos posts
    titulo= models.CharField(max_length=100)
    contenido= models.TextField()
    fecha_publicacion=models.DateTimeField(default=timezone.now)
    #actualizacion=models.DateTimeField(auto_now=True)
    # tipoPost=models.CharField(max_length=50)
    tematica= models.ManyToManyField(Tematica)
    estado= models.BooleanField('Publicado/NoPublicado', default=True)
    def __str__(self):
        return f'Posteo:   {self.titulo}, user: {self.posteador}'


class Likes(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)


class ComentariosPost(models.Model):
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    #foreignKey porque un comentario está en un SOLO post pero cada Post puede tener
    #muchos comentarios
    fecha= models.DateTimeField(default=timezone.now)
    contenido_comentario=models.TextField()
    comentarista= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="comentarista")
    #ForeignKey porque un comentario tiene un solo comentarista pero 
    #cada usuario puede hacer muchos comentarios
    def __str__(self):
        return f'Comentario:   {self.contenido_comentario} user: {self.comentarista}'
class VistaDelPost(models.Model):
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    visto= models.DateTimeField(auto_now_add=True)

class Favoritos(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    #ver que tipo de relacion tendria
class Avatar(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    imagen=models.ImageField(upload_to= 'avatares', null=True, blank=True)



