from audioop import reverse
from http.client import HTTPResponse
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.views.generic.list import ListView
from UserApp.forms import PostForm, TematicaForm, UserRegisterForm
from UserApp.models import Post, Tematica
from django.db.models import Q
# Create your views here.

def inicio(request):
    post=Post.objects.filter(estado=True)
    return render(request, 'inicio.html', {'post':post})




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
                        login(request, user)
                       
                        return render(request,"inicio.html",  {"mensaje":f"Bienvenido {usuario}"} )
                  else:
                        
                        return render(request,"inicio.html", {"mensaje":"Error, datos incorrectos"} )

            else:
                        
                        return render(request,"inicio.html" ,  {"mensaje":"Error, formulario erroneo"})

      form = AuthenticationForm()

      return render(request,"login.html", {'form':form} )

class CantViewPost(ListView):
    model = Post
    template= 'UserApp/viewPost.hmtl'


# class CrearPost2(CreateView):
#     model=Post
#     form_class= PostForm
#     template_name= 'crearPost.html'
#     success_url= reverse_lazy('inicio.html')


##### SECCION POST ####
def CrearPost(req):

    if req.method == "POST":
        miForm=PostForm(req.POST)
        if miForm.is_valid:
            post=miForm.save(commit=False)
            post.posteador=req.user
            post.save()
            return render(req, 'posteos.html',{"mensaje":"Tu post fue creado!"})
        else:
            return HTTPResponse('Los datos ingresados son incorrectos')
    else:
        miForm= PostForm()
    return render(req, 'crearPost.html',{'miForm':miForm})


def verTematicas(req):
    listaTematicas= Tematica.objects.all()
    return render(req,'tematicas.html',{"listaTematicas": listaTematicas})


#Es necesario hacer cada view para cada categoria? 
#Si tenemos categorias predefinidas es más fácil, sin embargo también se tiene que poder agregar tematicas
#Entonces...
#1)Se crea un Post
#2)Se elige o se crea la tematica
#3)Se guarda el post 
#4)Esa tematica agregada queda el template "tematicas.html"
#5)Presionar sobre uno me lleva a los posteos que tengan esa tematica

def verPosteos(req):
    post=Post.objects.filter(estado=True) #vemos si esta activo o no el post y filtramos los activos (True[1])
    print(post)
    return render(req,'posteos.html', {'post':post})

def buscarPosteos(req):
    return render(req, 'buscarPosteos.html')
def busquedaPosteos(req):
    if req.GET['titulo']:
        return HTTPResponse(req,'XD')
    else:
        respuesta="No enviaste datos"
    return HTTPResponse(respuesta)
####SECCION POST ####



####SECCION TEMATICAS####
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

# def buscarTematicas(req):
#     busqueda=req.GET.get("buscar")
#     tematica= Tematica.objects.all()
#     if busqueda:
#         posts=Post.objects.filter(
#             Q(nombre__icontains=busqueda)
#         )

def buscarTematicas(req):
    if req.GET['tematica']:
        tematica=req.GET['tematica']
        nombreTematica=Tematica.objects.filter(nombre__icontains=tematica)
        #No me está armando la lista... 
        return render(req, "resultados.html", {'tematicas':nombreTematica})
    else:
        respuesta="No enviaste datos"
    return HTTPResponse(respuesta)