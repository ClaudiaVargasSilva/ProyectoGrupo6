from django.urls import path
from UserApp import views
urlpatterns = [
    path('', views.inicio, name="inicio"),
   # path('padre', views.padre, name="padre"),
    path('login', views.Login, name="inicioSesion"),
    path('registro', views.register, name="registro"),
    #path('login2', views.Login2, name="login2"),
    path('Posteos', views.verPosteos, name="Posteos"),
    path('buscarPosteos', views.buscarPosteos, name="buscarPosteos"),
    path('busquedaPosteos', views.busquedaPosteos, name="busquedaPosteos"),
    path('Tematicas', views.verTematicas, name="tematicas"),
    path('crearPost',views.CrearPost, name ="crearPost"),
    path('crearTematica',views.CrearTematica, name="crearTematica"),
    path('buscarTematicas', views.buscarTematicas, name="buscarTematicas")
    #path('PostView', views.CantViewPost.as_view(), name="VistasPost")
]
