from itertools import count
from django.utils import timezone
from tkinter import CASCADE
from django.db import models
from django.conf import Settings,settings
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User




class Avatar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to= 'avatares', null=True, blank=True, default = 'PorDefecto/profileImageDefault.jpg' )
    
##Ver diferencia entre auth_user_model y model User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    imagenPerfil =models.ImageField(upload_to= 'avatares', null=True, blank=True, default = 'PorDefecto/profileImageDefault.jpg' )
    # avatar= models.OneToOneField(Avatar, on_delete=models.CASCADE)
    biografia = models.TextField(max_length=500, null=True, blank=True)
    #poner un atributo posteos? osea los posteos relacionados a cada usuario y se muestren en el perfil?
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
    imagenPost= models.ImageField(null=True, blank=True, upload_to = 'imagenes', max_length = 255)
    def __str__(self):
        return f'Posteo:   {self.titulo}, user: {self.posteador}'
    #     class A(model.Model):
    # blah = CharField(max_length=10)
    # profile = ImageField(
    #     upload_to='uploads/',
    #     default='uploads/default.jpg',
    #     blank=True
    # )
    # @property
    # def get_comment_count(self):
    #     return self.ComentariosPost_set.all().count()
    # @property
    # def get_view_count(self):
    #     return self.VistaDelPost_set.all().count()
    # @property
    # def get_like_count(self):
    #     return self.Likes_set.all().count()

class Likes(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    usuario=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


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

