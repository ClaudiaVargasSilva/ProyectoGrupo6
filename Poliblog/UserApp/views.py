from audioop import reverse
from collections import UserDict
from genericpath import exists
import numbers
from this import d
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from email.policy import default
from django.http import HttpResponse, JsonResponse
from urllib import request
from venv import create
from django.contrib.auth.models import User

from dataclasses import fields
from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LogoutView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
import random
from django.views.generic.edit import UpdateView, DeleteView
from UserApp.forms import PostForm, MensajeForm,MensajeForm2,RoomForm,PerfilForm,MensajeForm,TematicaForm, UserRegisterForm, UserEditForm,ComentarioForm, AvatarFormulario, ComentFormulario
from UserApp.models import Avatar,SolicitudAmistad,Room,MisMensajes , PostFavoritos,Likes,Post,Perfil, Tematica, ComentariosPost, Lenguaje

from django.db.models import Q
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy

# Create your views here.

def mantencion(req):
    return render(req, 'mantencion.html')

def enviarMensajeAdmin(req):
    pass


# def login2(req):
#     return render(req, 'login2.html')

def padre(req):
    return render(req, 'padre.html')


def register(request):

    if request.method == 'POST':

           #form = UserCreationForm(request.POST)
           form = UserRegisterForm(request.POST)
           if form.is_valid():
                 username = form.cleaned_data['username']
                 user = form.save()
                 bio = form.cleaned_data['biografia']
                #  avatar= Avatar(user=request.user)
                #  perfil=Perfil(user=request.user , avatar = avatar)
                 avatar = Avatar.objects.create(
                     user = user,
                    #  imagen = None
                 )
                 Perfil.objects.create(
                     user = user,
                     biografia = form.cleaned_data['biografia']
                 )
                 
                 return render(request,"usuarioCreado.html" ,  {"mensaje":"Usuario Creado :)"})

    else:
            #form = UserCreationForm()       
            print("No se creo nada")
            form = UserRegisterForm()     

    return render(request,"registro.html" ,  {"form":form})

def Login(request):
    post=Post.objects.all()
    listaTematicas=Tematica.objects.all()

    if request.method == "POST":
            form = AuthenticationForm(request, data = request.POST)

            if form.is_valid():
                  usuario = form.cleaned_data.get('username')
                  contra = form.cleaned_data.get('password')
                #username y password son las keys del form de django para el login?
                #osea a usuario y contra asiganamos el valor del formulario
                  user = authenticate(username=usuario, password=contra)
                  #con la sentencia de arriba comparamos si los campos coinciden con los campos de
                  #del modelo User, siempre y cuando tengamos usuarios registrados
                  if user is not None:
                    login(request, user) #
                    messages.success(request,'Bienvenido!' )
                    #return render(request,"inicio.html",  {"mensaje":f"Bienvenido {usuario}", "post":post, "lista":listaTematicas} )
                    return redirect(inicio)
                  else:
                    # return render(request,"inicio.html", {"mensaje":"Error, datos incorrectos","post":post, "lista":listaTematicas} )
                    return render(request, "loginError.html",{'mensaje': "Error! Datos erróneos"})

            else:
                # return render(request,"inicio.html" ,  {"mensaje":"Error, formulario erroneo","post":post, "lista":listaTematicas})
                return render(request, "loginError.html",{'mensaje': "Error! Datos erróneos"})
    form = AuthenticationForm()
    return render(request,"login.html", {'form':form} )

def eliminarCuenta(req):
    pass



def verPerfil(req):
    usuario = req.user
    perfil = Perfil.objects.filter(user=usuario)
    post= Post.objects.filter(posteador=usuario)

    username= usuario.username
    userBio= usuario.perfil.biografia
    email= usuario.email
    avatar= usuario.perfil.imagenPerfil
    print(username)
    print(post)

    return render(req, "perfil.html", {'username':username,'email':email,'biografia':userBio, 'usuario':usuario,'post':post})


def perfil2(req):
    return render(req, "perfil2.html")

def agregarAvatar(request):
      if request.method == 'POST':

            miFormulario = AvatarFormulario(request.POST, request.FILES)

            if miFormulario.is_valid():


                #   u = User.objects.get(username=request.user)
                  user= request.user
                  imagen=miFormulario.cleaned_data['imagen']
                  avatar = Avatar (user=user, imagen=imagen) 
                #   imagenNueva= Perfil
      
                  avatar.save()

                  return render(request, "perfil.html", {'avatar':avatar.imagen.url}) 

      else: 

            miFormulario= AvatarFormulario() 

      return render(request, "agregarAvatar.html", {"miFormulario":miFormulario})


def actualizarAvatar(request):
    pass

def iniciarChat(req):
    return render(req, 'chat.html')

def otroPerfil(req, id):
    otroUser = User.objects.get(id=id) #recuperar la id del otro perfil
    postsDelOtroUser= Post.objects.filter(posteador=otroUser)
    print(otroUser)
    print(postsDelOtroUser)
    perfil = Perfil.objects.get(user=otroUser)
    
    return render(req,'otroPerfil.html', {'otroUser': otroUser,'perfil':perfil, 'posts': postsDelOtroUser})

def verAmigos(req):
    perfil = Perfil.objects.get(user=req.user)
    amigos = perfil.amigos
    solicitudes = SolicitudAmistad.objects.filter(to_user=req.user)
    print(amigos)
    return render(req, 'amigos.html', {'amigos':amigos, 'solicitudes':solicitudes})
def eliminarAmigos(req):
    pass

def enviarSolicitud(req, id):
    from_user = req.user
    to_user = User.objects.get(id=id)
    SolicitudAmistad.objects.get_or_create(from_user= from_user, to_user = to_user)
    return HttpResponse('solicitud enviada')

def aceptarSolicitud(req, id):
    solicitudAmistad = SolicitudAmistad.objects.get(id= id)
    to_user = req.user
    from_user = solicitudAmistad.from_user
    perfil_to_user=Perfil.objects.get(user = to_user )
    perfil_from_user= Perfil.objects.get( user = from_user)
    
    if solicitudAmistad.to_user == req.user:
        solicitudAmistad.to_user.perfil.amigos.add(solicitudAmistad.from_user)
        solicitudAmistad.from_user.perfil.amigos.add(solicitudAmistad.to_user)
        solicitudAmistad.delete()
        return HttpResponse('solicitud de amistad aceptada') #la idea seria utilizar django.messages o un modal
   
def rechazarSolicitud(req, id):
    solicitudAmistad = SolicitudAmistad.objects.get(id= id)
    solicitudAmistad.delete()
    return HttpResponse('solicitud de amistad eliminada') #la idea seria utilizar django.messages o un modal


def enviarMensaje(req,id):
    destinatario = User.objects.get(id=id)
    if req.method == "POST":
        miForm=MensajeForm(req.POST)
        # print(req.FILES['imagenPost'])
        if miForm.is_valid:
            mensaje=miForm.save(commit=False)
            mensaje.user=req.user
            mensaje.destinatario= destinatario
            mensaje.save()
            miForm.save_m2m()
            return redirect(inicio)
        else:
            return HttpResponse('Los datos ingresados son incorrectos')
    else:
        miForm= MensajeForm()
    return render(req, 'crearMensaje.html',{'miForm':miForm,'destinatario':destinatario})


def crearMensaje(req): 
    return render(req, 'crearMensaje2.html')


def crearMensaje2(req):
    destino = req.POST['destinatario']
    mensaje = req.POST['mensaje']
    # destinoFinal = User.objects.get(username=destino)
    if User.objects.filter(username=destino).exists():
        destinoFinal = User.objects.get(username=destino)
        MisMensajes.objects.create(user=req.user, mensaje=mensaje, destinatario=destinoFinal)
        return HttpResponse("mensaje enviado!")
    else:
        return HttpResponse('el usuario destino no existe!')
    

def verMensajes(req):
    
    destinatario = req.user
    # perfil =Perfil.objects.get(user= usuario)
    # print(perfil)
    # mensaje = MisMensajes.objects.filter(destinatario = perfil)
    mensaje = MisMensajes.objects.filter(destinatario=destinatario)
    return render(req, 'mensajesDirectos.html', {
        'mensaje':mensaje
        
    })
def verMensajesEnviados(req):
    mensajes= MisMensajes.objects.filter(user=req.user)
    return render(req, 'mensajesEnviados.html', {'mensajes':mensajes})

def verMensajeEspecifico(req,id):
    mensajeEsp = MisMensajes.objects.get(id=id)
    return render(req, 'mensajeEspecifico.html', {'mensajeEsp':mensajeEsp})

def eliminarMensaje(req,id):
    mensajeEliminar=MisMensajes.objects.get(id=id)
    #faltaria un template o MODAL que diga si estoy seguro y asi
    #faltaria que si borro un mensaje que ENVIÉ que se borre de ambas partes pero si elimino un mensaje que RECIBI que se me borre a mi pero no a la otra persona...
    mensajeEliminar.delete()
    return redirect(inicio)

def guardarMensaje(req):
    pass
def buscarMensaje(req):
    pass



def editarUsuario(req):
    usuario = req.user
    perfil = req.user.perfil
    # perfil = Perfil.objects.filter(user=usuario)
    if req.method == 'POST':
        miForm = UserEditForm(req.POST, instance = usuario)
        miPerfil= PerfilForm(req.POST, req.FILES, instance=perfil)
        if miForm.is_valid() and miPerfil.is_valid():
            info= miForm.cleaned_data
            perfil1 = miPerfil.cleaned_data
            usuario.email = info['email']
            usuario.first_name= info['first_name']
            usuario.last_name= info['last_name']
            new_password = info['password1']
            usuario.set_password(new_password)
            perfil.imagenPerfil= perfil1['imagenPerfil'] #esto no me actualiza
            perfil.biografia = perfil1['biografia']
            miPerfil.save()
            usuario.save()
            # miPerfil.save_m2m()
            return redirect(inicio)
    else:
        miForm = UserEditForm(initial={'email': usuario.email,'first_name':usuario.first_name ,'last_name': usuario.last_name,'password':usuario.password})
        miPerfil = PerfilForm(instance=perfil)
        return render(req, 'editarPerfil.html',{'miForm':miForm, 'miPerfil': miPerfil,'usuario':usuario})


def mensajes(req):
    return render(req,'mensajesDirectos.html')



def idPost(id): #devuelve la id de cada POST
    return Post.objects.get(id=id)
    



def inicio(request):
    post=Post.objects.all() #devuelve una lista de posteos
    listaTematicas=Tematica.objects.all() #devuelve una lista
    page=request.GET.get('page',1)
    paginator = Paginator(post,4)
    try:
        posteos=paginator.page(page)
    except PageNotAnInteger:
        posteos=paginator.page(1)
    except EmptyPage:
        posteos= paginator.page(paginator.num_pages)
    contexto={
        'post':post,
        'lista': listaTematicas,
        'posteos':posteos
    }
    if not request.user.is_authenticated:
        return render(request, 'inicio.html', contexto)
    else:
        return render(request, 'inicio.html', contexto)


    


def verPosteos(req,id):
    post=Post.objects.get(id=id)
    comentario= ComentariosPost.objects.filter(post__id=id) #si uso GET devuelve una lista? No, no devuelve una lista
    #entonces uso filter :D
    tematicas=Tematica.objects.filter(post__id=id) #tematicas asociadas al Post solicitado
    lista= Tematica.objects.all()

    if req.method=="POST":
        miFormComentario=ComentarioForm(req.POST)
        
        if miFormComentario.is_valid:
            comentarioNuevo= miFormComentario.save(commit=False)
            comentarioNuevo.comentarista= req.user
            comentarioNuevo.post=post
            comentarioNuevo.save()
        else:
            return HttpResponse("No funcionaaaaaaa")
    else:
        miFormComentario=ComentarioForm()
    return render(req,'posteos.html', {'post':post, 'tematicas':tematicas, 'comentario':comentario, 'miFormComentario': miFormComentario, 'lista':lista})


def darLike(req,id):
    post = get_object_or_404(Post, id=id)
    likes = Likes.objects.filter(usuario=req.user, post=post)
    if likes.exists():
        likes.delete()
        return redirect('Posteos',id=id)
    Likes.objects.create(usuario=req.user, post=post)
    return redirect('Posteos',id=id)

def verLikes(req):
    likes = Likes.objects.filter(usuario=req.user)
    
    return render(req, "misLikes.html", {'likes':likes})

def postFavoritos(req, id):
    post= get_object_or_404(Post, id=id)
    postFav= PostFavoritos.objects.filter(user=req.user, post=post)
    if postFav.exists():
        postFav.delete()
        return redirect('Posteos', id=id)
    PostFavoritos.objects.create(user=req.user,post=post)
    return redirect('Posteos',id=id)

def verPostFavoritos(req):
    postFav= PostFavoritos.objects.filter(user=req.user)
    return render(req, 'misPostGuardados.html',{'postFav':postFav})

@login_required
def CrearPost(req):

    if req.method == "POST":
        miForm=PostForm(req.POST, req.FILES)
        if miForm.is_valid:
            post=miForm.save(commit=False)
            post.posteador=req.user
            post.save()
            miForm.save_m2m()
            return redirect(inicio)
        else:
            return HttpResponse('Los datos ingresados son incorrectos')
    else:
        miForm= PostForm()
    return render(req, 'crearPost.html',{'miForm':miForm})


def busquedaPost(req):
    return render(req, "UserApp/busquedaPost.html")

def buscar(request):
    if request.GET['titulo']:
        respuesta  = f"Buscando : {request.GET['titulo']}"
        print("AAAAAAAAAAAAA")
        print(respuesta)

        titulo     = request.GET['titulo']
        post       = Post.objects.filter(titulo__icontains=titulo)
        return render(request, 'UserApp/resultadosBusqueda.html', {"post": post, "titulo":titulo })
    else:
        respuesta = "No hay datos"

    return HttpResponse(respuesta)





####SECCION TEMATICAS####
def verTematicas(req):
    listaTematicas= Tematica.objects.all()
    return render(req,'tematicas.html',{"listaTematicas": listaTematicas})

class TematicaCreate(CreateView):
    model=Tematica
class TematicaList(ListView):
    model= Tematica
    template_name= "tematicas_List.html"

class TematicaDetail(DetailView):
    model= Tematica
    template_name="tematicas_detalle.html"

class TematicaUpdate(UpdateView):
    model=Tematica
    success_url= 'UserApp/tematicasList'
    fields= ['nombre']
class TematicaDelete(DeleteView):
    model= Tematica
    success_url=  reverse_lazy('tematicasList') #Ver por qué no me lleva a la url correspondiente...
    template_name= "tematica_delete.html"
def postRelacionados(req, pk):
    
    post= Post.objects.filter(tematica__id=pk)

    return render(req,'postRelacionados.html', {'postRelacionados' : post})

def CrearTematica(req):

    if req.method== 'POST':
        miForm=TematicaForm(req.POST)
        if miForm.is_valid:
            miForm.save()
            return redirect(inicio)
        else:
            return HttpResponse('Los datos ingresados son incorrectos')
    else:
        miForm=TematicaForm()
    
    return render(req, 'crearTematica.html',{'miForm': miForm})


def buscarTematicas(req):
    if req.GET['tematica']:
        tematica=req.GET['tematica']
        nombreTematica=Tematica.objects.filter(nombre__icontains=tematica)
        #No me está armando la lista... 
        return render(req, "resultados.html", {'tematicas':nombreTematica})
    else:
        respuesta="No enviaste datos"
    return HttpResponse(respuesta)

def eliminarTematicas(req, id_tematica):
    tematica= Tematica.objects.get(id=id_tematica)
    tematica.delete()
    listaTematicas= Tematica.objects.all()
    return render(req, 'tematicas.html',{'listaTematicas': listaTematicas})
    # return redirect(tematicas)

def editarTematicas(req, id_tematica):
    tematica= Tematica.objects.get(id=id_tematica)
    listaTematicas= Tematica.objects.all()
    if req.method=='POST':
        miForm= TematicaForm(req.POST)
        if miForm.is_valid:
            info=miForm.cleaned_data
            tematica.nombre= info['nombre']
            tematica.save()
            return render(req, 'tematicas.html',{'listaTematicas': listaTematicas}) 
    else:
        miForm= TematicaForm(initial={'nombre':tematica.nombre})
    return render(req, 'editarTematicas.html',{'miForm':miForm})

###SECCION COMENTARIOS###

def verComentarios(req):
    comentario= ComentariosPost.objects.filter(comentarista=req.user)
   
    return render(req, 'comentarios.html', {'comentario':comentario})

def eliminarComentario(req, id_comentario):
    comentario= ComentariosPost.objects.get(id=id_comentario)
    comentario.delete()
    comentarioCompleto= ComentariosPost.objects.filter(comentarista=req.user) 
    return render(req, 'comentarios.html', {'comentario':comentarioCompleto})

def editarComentario(req, id_comentario):
    comentario = ComentariosPost.objects.get(id=id_comentario)
    if req.method=="POST":

        miFormComentario = ComentarioForm(req.POST) 
        print(miFormComentario)
        if miFormComentario.is_valid:
            informacion                     = miFormComentario.cleaned_data
            comentario.contenido_comentario = informacion['contenido_comentario']
            comentario.save()
        else:
            return HttpResponse("No funcionaaaaaaa")

    else: 
        miFormComentario= ComentarioForm(initial={'contenido_comentario': comentario.contenido_comentario}) 
        
    return render(req, "editarComentario.html", {"miFormulario":miFormComentario, "id_comentario":id_comentario})
    

class LenguajeCreate(CreateView):
    model= Lenguaje
    fields=['nombreLenguaje']
    success_url= '/UserApp/'
    template_name = "lenguaje_form.html"


###SECCION CRUD###
@login_required
def leerposts(req):
    post = Post.objects.all()
    contexto = {"post": post}

    return render(req, 'buscar_post.html', contexto)



class listaPost(ListView):
    model = Post
    template_name = "buscar_post.html"
    def get_context_data(self,*args, **kwargs):
        context = super(listaPost, self).get_context_data(*args,**kwargs)
        context['posts'] = Post.objects.filter(posteador=self.request.user)
        return context
    # def get(self,req):
    #     context:{}

    #     post= Post.objects.filter(posteador=req.user)
    #     return context:{'post':post}
    #filtrar pero por los posteos del, que no aparezcan todos
class detallePost(DetailView):
    model = Post
    template_name = "detalle_post.html"


class actualizaPost(UpdateView):
    model = Post
    success_url = "/UserApp/listaPost"
    fields = ["titulo","subtitulo", "contenido", "tematica", "imagenPost"]
    success_message = 'Post editado!'

class postCreate(CreateView):
    model = Post
    fields = ["posteador", "titulo", "subtitulo", "contenido", "fecha_publicacion", "tematica", "estado", "imagenPost"]
    success_url = '/UserApp/listaPost'

class eliminaPost(DeleteView):
    model = Post
    success_url = '/UserApp/listaPost'
    template_name = 'post_confirm_delete.html'