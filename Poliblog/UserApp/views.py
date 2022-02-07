from audioop import reverse
from collections import UserDict
from email.policy import default
from http.client import HTTPResponse
from venv import create
from dataclasses import fields
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LogoutView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from django.views.generic.edit import UpdateView, DeleteView
from UserApp.forms import PostForm, PerfilForm,TematicaForm, UserRegisterForm, UserEditForm,ComentarioForm, AvatarFormulario
from UserApp.models import Avatar,Post,Perfil, Tematica, ComentariosPost, Lenguaje
from django.db.models import Q
from django.views.generic.detail import DetailView

from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy

# Create your views here.

def mantencion(req):
    return render(req, 'mantencion.html')



def login2(req):
    return render(req, 'login2.html')

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


# def verPerfil(req):
#     usuario= Perfil.user.get_object()
#     return render(req, 'perfil.html',{'usuario':usuario})

def verPerfil(req):
    usuario = req.user
    perfil = Perfil.objects.filter(user=usuario)
    post= Post.objects.filter(posteador=usuario)

    username= usuario.username
    userBio= usuario.perfil.biografia
    email= usuario.email
    avatar= usuario.perfil.imagenPerfil
    
    #Cuando el usuario actualice su avatar que borre el por defecto !

    # avatar= usuario.perfil.avatar



    # perfilBio= perfil.biografia
    # print(userBio)
    print(username)
    print(post)
    # print(perfilBio)
        # avatares=Avatar.objects.filter(user=request.user.id)

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
            # perfil.user= usuario
            perfil.imagenPerfil= perfil1['imagenPerfil'] #esto no me actualiza
            perfil.biografia = perfil1['biografia']
            # usuario.password1 = info['password1']
            # usuario.password2 = info['password2']
            # usuario.perfil.imagenPerfil = info['imagenPerfil']
            
            # Perfil.objects.update(
            #     imagenPerfil = info['imagenPerfil'] 
            # )
            # perfil.imagenPerfil= info['imagenPerfil']
            
            # perfil=miPerfil.save(commit=False)
            # perfil.user = req.user
            miPerfil.save()
            usuario.save()
            # miPerfil.save_m2m()
            return redirect(inicio)
    else:
        miForm = UserEditForm(initial={'email': usuario.email,'first_name':usuario.first_name ,'last_name': usuario.last_name,'password':usuario.password})
        miPerfil = PerfilForm(instance=perfil)
        return render(req, 'editarPerfil.html',{'miForm':miForm, 'miPerfil': miPerfil,'usuario':usuario})



def idPost(id): #devuelve la id de cada POST pasandole el id del Post
    return Post.objects.get(id=id)
    



def inicio(request):
    post=Post.objects.all()
    avatares=Avatar.objects.filter(user=request.user.id)
    # print(Post.objects.filter(id))
    post1=list(Post.objects.filter(
        estado=True
    ).values_list('id', flat=True))
    print(post1) #post1 me devuelve una LISTA con las ID de los POSTS
    # post2=idPost(post1)
    # print(post2)
    # listaTematicasPost=[]
    # tematicas=[]
    
    listaTematicas=Tematica.objects.all() #devuelve una lista
    # for i in post1:
    #     postResult= idPost(i) 
    #     print(postResult)
    #     tematicas= Tematica.objects.filter(post__id=postResult.id)   
    #     print(tematicas) 
    #     listaTematicasPost.append(tematicas)
    # print(listaTematicasPost) #lista de tematicas de CADA POST ordenados por id...si borro un post, como quedaria????, si yo la paso como está me muestra la lista nomás...
    # print(tematicas) #me imprime la ultima tematica del ultimo Post....
    
    # listaTematicasPost= Tematica.objects.filter(post__id=post1.id)
    # listaTematicasPost=Tematica.objects.filter(post__id=id(post.i))
    #en listaTematicasPost me tiene que devolver las tematicas del post que aparece en el inicio
    if not request.user.is_authenticated:
        return render(request, 'inicio.html', {'post':post, 'lista':listaTematicas})
    else:
        return render(request, 'inicio.html', {'post':post, 'lista':listaTematicas})


def verPosteos(req,id):
    post=Post.objects.get(id=id)
    comentario= ComentariosPost.objects.filter(post__id=id) #si uso GET devuelve una lista? No, no devuelve una lista
    #entonces uso filter :D
    tematicas=Tematica.objects.filter(post__id=id) #tematicas asociadas al Post solicitado

    if req.method=="POST":
        miFormComentario=ComentarioForm(req.POST)
        
        if miFormComentario.is_valid:
            comentarioNuevo= miFormComentario.save(commit=False)
            comentarioNuevo.comentarista= req.user
            comentarioNuevo.post=post
            comentarioNuevo.save()
        else:
            return HTTPResponse("No funcionaaaaaaa")
    else:
        miFormComentario=ComentarioForm()
    return render(req,'posteos.html', {'post':post, 'tematicas':tematicas, 'comentario':comentario, 'miFormComentario': miFormComentario})






def CrearPost(req):

    if req.method == "POST":
        miForm=PostForm(req.POST, req.FILES)
        # print(req.FILES['imagenPost'])
        if miForm.is_valid:
            post=miForm.save(commit=False)
            post.posteador=req.user
            # post.imagenPost= req.FILES['imagenPost']
            # post.imagenPost= miForm.cleaned_data['imagenPost']
            # post.imagenPost= miForm[imagenPost]
            post.save()
            miForm.save_m2m()
            # return render(req, 'inicio.html',{"mensaje":"Tu post fue creado!"})
            return redirect(inicio)
        else:
            return HTTPResponse('Los datos ingresados son incorrectos')
    else:
        miForm= PostForm()
    return render(req, 'crearPost.html',{'miForm':miForm})

# class PostCreate(CreateView):
#     model=Post
#     fields=['titulo','contenido','tematica']
#     success_url='UserApp/inicio'

# VER COMO 





def buscarPosteos(req):
    return render(req, 'buscarPosteos.html')
def busquedaPosteos(req):
    if req.GET['titulo']:
        return HTTPResponse(req,'XD')
    else:
        respuesta="No enviaste datos"
    return HTTPResponse(respuesta)



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


def CrearTematica(req):

    if req.method== 'POST':
        miForm=TematicaForm(req.POST)
        if miForm.is_valid:
            miForm.save()
            return render(req, 'inicio.html')
        else:
            return HTTPResponse('Los datos ingresados son incorrectos')
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
    return HTTPResponse(respuesta)

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

def verComentarios(req,id):
    comentario= ComentariosPost.objects.get(id=id)
   
    return render(req, 'comentarios.html', {'comentario':comentario})





class LenguajeCreate(CreateView):
    model= Lenguaje
    fields=['nombreLenguaje']
    success_url= '/UserApp/'
    template_name = "lenguaje_form.html"


###SECCION CRUD###
def leerposts(req):
    post = Post.objects.all()
    contexto = {"post": post}

    return render(req, 'buscar_post.html', contexto)

class listaPost(ListView):
    model = Post
    template_name = "buscar_post.html"

class detallePost(DetailView):
    model = Post
    template_name = "detalle_post.html"


class actualizaPost(UpdateView):
    model = Post
    success_url = "/UserApp/listaPost"
    fields = ["titulo","contenido", "tematica", "imagenPost"]
    success_message = 'Post editado!'

class postCreate(CreateView):
    model = Post
    fields = ["posteador", "titulo","contenido", "fecha_publicacion", "tematica", "estado", "imagenPost"]
    success_url = '/UserApp/listaPost'

class eliminaPost(DeleteView):
    model = Post
    success_url = '/UserApp/listaPost'
    template_name = 'post_confirm_delete.html'