from django.urls import path
from UserApp import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.inicio, name="inicio"),
   # path('padre', views.padre, name="padre"),
    path('login', views.Login, name="inicioSesion"),
    path('registro', views.register, name="registro"),
    path('logout', LogoutView.as_view(next_page="inicioSesion"), name="Logout"),
    path('login2', views.login2, name="login2"),
    #path('login2', views.Login2, name="login2"),
    
    path('Posteos/<id>', views.verPosteos, name="Posteos"),
    path('buscarPosteos', views.buscarPosteos, name="buscarPosteos"),
    path('busquedaPosteos', views.busquedaPosteos, name="busquedaPosteos"),
    path('comentarios/<id>', views.verComentarios, name="comentarios"),
    path('crearPost',views.CrearPost, name ="crearPost"),

    path('leerPosts/', views.leerposts, name="leerPosts"),
    path('listaPost', views.listaPost.as_view(), name='listaPost'),
    path('actualizaPost/<pk>/', views.actualizaPost.as_view(), name='actualizaPost'),
    path('eliminaPost/<pk>/', views.eliminaPost.as_view(), name='eliminaPost'),
    
    path('Tematicas', views.verTematicas, name="tematicas"),
    path('crearTematica',views.CrearTematica, name="crearTematica"),
    path('buscarTematicas', views.buscarTematicas, name="buscarTematicas"),

    path('crearLenguajes', views.LenguajeCreate.as_view(), name='New'),
    #path('PostView', views.CantViewPost.as_view(), name="VistasPost")
]
