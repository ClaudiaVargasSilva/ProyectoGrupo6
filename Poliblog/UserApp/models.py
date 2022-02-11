from itertools import count
from operator import truediv
from django.utils import timezone
from tkinter import CASCADE
from django.db import models
from django.conf import Settings,settings
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import uuid



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
    
    titulo= models.CharField(max_length=100)
    contenido= models.TextField()
    fecha_publicacion=models.DateTimeField(default=timezone.now)
    
    tematica= models.ManyToManyField(Tematica)
    estado= models.BooleanField('Publicado/NoPublicado', default=True)
    imagenPost= models.ImageField(null=True, blank=True, upload_to = 'imagenes', max_length = 255)
    def __str__(self):
        return f'Posteo:   {self.titulo}, posteador: {self.posteador}'

    def get_tematica(self):
        tematicas= self.tematica.all()
        return tematicas
    def get_comment_count(self):
        return self.comentariospost_set.all().count()
    def get_view_count(self):
        return self.vistadelpost_set.all().count()
    def get_like_count(self):
        return self.likes_set.all().count()

class Likes(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    usuario=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'Like de: {self.usuario}, post= {self.post.titulo}'
class ComentariosPost(models.Model):
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    #foreignKey porque un comentario está en un SOLO post pero cada Post puede tener
    #muchos comentarios
    fecha= models.DateTimeField(default=timezone.now)
    contenido_comentario=models.TextField()
    comentarista= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="comentarista")
    
    def __str__(self):
        return f'Comentario:   {self.contenido_comentario} user: {self.comentarista}'
class VistaDelPost(models.Model):
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    visto= models.DateTimeField(auto_now_add=True)

class PostFavoritos(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return f'Fav de: {self.user}, post= {self.post}'
    #un favorito tiene un usuario pero un usuario puede tener muchos favs
    
    #ver que tipo de relacion tendria

######## Mensajes directos #########

# class ModelBase(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True, db_index= True, editable = False)
#     tiempo = models.DateTimeField(auto_now_add=True)
#     actualizar = models.DateTimeField(auto_now_add= True)
#     class Meta():
#         abstract = True
#     #no creara ninguna base de datos pues este modelo base es ABSTRACTO

# class CanalMensajes(ModelBase):
#     canal = models.ForeignKey("Canal", on_delete=models.CASCADE)
#     usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     texto = models.TextField()

# class CanalUsusario(ModelBase):
#     canal = models.ForeignKey("Canal", on_delete=models.SET_NULL)
#     usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


# class Canal(ModelBase):
#     usuario =models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, through=CanalUsusario)