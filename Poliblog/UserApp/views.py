from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.views.generic.list import ListView
from UserApp.models import Post
# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')


def verPosteos(req):
    return render(req, 'posteos.html')
def padre(req):
    return render(req, 'padre.html')
def Login(request):
    
      if request.method == "POST":
            form = AuthenticationForm(request, data = request.POST)

            if form.is_valid():
                  usuario = form.cleaned_data.get('username')
                  contra = form.cleaned_data.get('password')
                #username y password son las keys del form de django para el login?
                  user = authenticate(username=usuario, password=contra)

            
                  if user is not None:
                        login(request, user)
                       
                        return render(request,"AppCoder/inicio.html",  {"mensaje":f"Bienvenido {usuario}"} )
                  else:
                        
                        return render(request,"AppCoder/inicio.html", {"mensaje":"Error, datos incorrectos"} )

            else:
                        
                        return render(request,"AppCoder/inicio.html" ,  {"mensaje":"Error, formulario erroneo"})

      form = AuthenticationForm()

      return render(request,"AppCoder/login.html", {'form':form} )



class CantViewPost(ListView):
    model = Post
    template= 'UserApp/viewPost.hmtl'

# def register(request):

#       if request.method == 'POST':

#             #form = UserCreationForm(request.POST)
#             form = UserRegisterForm(request.POST)
#             if form.is_valid():

#                   username = form.cleaned_data['username']
#                   form.save()
#                   return render(request,"AppCoder/inicio.html" ,  {"mensaje":"Usuario Creado :)"})


#       else:
#             #form = UserCreationForm()       
#             form = UserRegisterForm()     

#       return render(request,"AppCoder/registro.html" ,  {"form":form})