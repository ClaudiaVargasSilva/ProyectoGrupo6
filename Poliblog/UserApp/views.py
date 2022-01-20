from audioop import reverse
from http.client import HTTPResponse
from venv import create
from dataclasses import fields
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LogoutView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView, DeleteView
from UserApp.forms import PostForm, TematicaForm, UserRegisterForm, ComentarioForm
from UserApp.models import Avatar,Post, Tematica, ComentariosPost, Lenguaje
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.




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
                 form.save()
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
                    return render(request,"inicio.html", {"mensaje":"Error, datos incorrectos","post":post, "lista":listaTematicas} )

            else:
                return render(request,"inicio.html" ,  {"mensaje":"Error, formulario erroneo","post":post, "lista":listaTematicas})
    form = AuthenticationForm()
    return render(request,"login.html", {'form':form} )
       



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
    #Hacer un if que verifique si el post TIENE comentarios o no, si tiene crea el objeto y el contexto si no tiene no pasa nada, ya que 
    #ahora NO me deja ver un posteo si NO tiene comentarios
    
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
        miForm=PostForm(req.POST)
        if miForm.is_valid:
            post=miForm.save(commit=False)
            post.posteador=req.user
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

###SECCION COMENTARIOS###

def verComentarios(req,id):
    comentario= ComentariosPost.objects.get(id=id)
   
    return render(req, 'comentarios.html', {'comentario':comentario})





class LenguajeCreate(CreateView):
    model= Lenguaje
    fields=['nombreLenguaje']
    success_url= '/UserApp/'
    template_name = "lenguaje_form.html"