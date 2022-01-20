from django.utils import timezone
from tkinter import CASCADE
from django.db import models
from django.conf import Settings,settings
#from django.contrib.auth.models import AbstractUser

# Una vez que hayamos decidido cuáles serán nuestros modelos y sus campos, debemos pensar en la relación que existe entre ellos. Django le permite definir relaciones de uno a uno 
# (OneToOneField), de uno a muchos (ForeignKey) y de muchos a muchos (ManyToManyField).
class Usuario(models.Model):
    nombre= models.CharField("nombre", max_length=100)
    apellido=models.CharField("apellido", max_length=100)
    email= models.EmailField()
    temas_favoritos= models.CharField("temasFav", max_length=100)
    #tematica= models.ManyToManyField("tematicas", max_length=50)
# class User(AbstractUser):
#     pass


##### Usamos clase abstracta User que viene en django y uso lo vinculamos con PERFIL(otro modelo)
##eso verlo para la entrega final

#Si después queremos agregar atributos o manipular el modelo User que viene por defecto en Django usamos Proxy, entre otros
#

class Tematica(models.Model):
    nombre=models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombre}'
#tematicas en que momento se agrega? Se agrega como algo aparte? un html solo para tematica no estaria bien, deberia ser un campo cuando se postea y que el valor que ingrese el usuario
#cuando escriba el Post, viaje a la tabla Tematica, como hacemos eso? Igual algunas tematicas podriamos agregar desde el admin, 
#YA SE, agregamos algunas tematicas, que se vea como un menu desplegable, una lista y de ahi elija y tambien pueda agregar
class Lenguaje(models.Model):
    nombreLenguaje=models.CharField(max_length=50)
#Lo mismo con lenguaje, si bien de algun se podria detectar automaticamente, ahora lo ideal seria igual que tematica, lista de lenguajes y poder agregar alguno
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
    #mantyToManyField porque un post puede abarcar distintas tematicas

#Posteo se agrega cuando en algun formulario de estilo posteo, cuando presione enviar se crea el posteo con cada uno de los atributos 

class Likes(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)

#ni idea esta, ver despues que onda

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
#comentarios lo mismo que Posteo
class VistaDelPost(models.Model):
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    visto= models.DateTimeField(auto_now_add=True)

#osea para agregar a favoritos o algo asi?
class Favoritos(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    #ver que tipo de relacion tendria
#ni idea esta
class Avatar(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    imagen=models.ImageField(upload_to= 'avatares', null=True, blank=True)



#Para la PreEntrega hacemos que el usuario se pueda registrar, que pueda postear y comentar...
#Al fin y al cabo estamos usando la herencia html, lo que es CRUD aprox y tenemos más de un modelo
#Podemos dar de alta el usuario, sin embargo estariamos adelantados a la clase 23...
#pero si agregamos usuarios de manera manual como un formulario no pisaria la tabla que viene por defecto en django?
#Que es lo que si o si podriamos rellenar con datos? 
#--> Posteos seguro
#--> Tematicas
#--> Lenguajes
#El primero ver como funcionaria el tema de foreigKey, etc

#Y buscar que sea por tematica y que muestre los posteos que tengan esa tematica
