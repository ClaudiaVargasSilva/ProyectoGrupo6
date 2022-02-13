from django.urls import path, include
from UserApp import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('nosotros', views.mantencion, name="nosotros"),

   # path('padre', views.padre, name="padre"),
    path('login', views.Login, name="inicioSesion"),
    path('registro', views.register, name="registro"),
    path('logout', LogoutView.as_view(next_page="inicioSesion"), name="Logout"),
    path('perfil', views.verPerfil, name="Perfil"),
    path('perfil2', views.perfil2, name="perfil2"),
    path('editarPerfil', views.editarUsuario, name="editarPerfil"),
    path('agregarAvatar', views.agregarAvatar, name="agregarAvatar"),
    #path('login2', views.Login2, name="login2"),
    path('mensajes', views.mensajes, name="misMensajes"),  
    path('Posteos/<id>', views.verPosteos, name="Posteos"),
    path('comentarios', views.verComentarios, name="comentarios"),
    path('chat', views.iniciarChat, name="chat"),
 
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('<str:room>/send', views.send, name='send'),
    path('<str:room>/getMessages/<id>', views.getMessages, name='getMessages'),
   

    path('busquedaPost/', views.busquedaPost, name="busquedaPost"),
    path('buscar/', views.buscar), 

    path('eliminarComentario/<id_comentario>',views.eliminarComentario, name="eliminarComentario"),
    path('editarComentario/<id_comentario>/', views.editarComentario, name="editarComentario"),

    path('likes/<id>', views.darLike, name="Likes"),
    path('misLikes', views.verLikes, name="verLikes"),
    path('guardados/<id>', views.postFavoritos, name="Postfavoritos"),
    path('misPostsGuardados', views.verPostFavoritos, name="verPostFavoritos"),

    #path('eliminarComentarios/<id>', views.eliminarComentarios, name="eliminarComentarios"),

    path('crearPost',views.CrearPost, name ="crearPost"),

    path('leerPosts/', views.leerposts, name="leerPosts"),
    path('listaPost', views.listaPost.as_view(), name='listaPost'),
    path('actualizaPost/<pk>/', views.actualizaPost.as_view(), name='actualizaPost'),
    path('eliminaPost/<pk>/', views.eliminaPost.as_view(), name='eliminaPost'),
    
    path('Tematicas', views.verTematicas, name="tematicas"),
    path('tematicasList', views.TematicaList.as_view(), name="tematicasList"),
    path('tematicasDetail/<pk>',views.TematicaDetail.as_view(), name="tematicasDetail"),
    path('tematicasUpdate/<pk>',views.TematicaUpdate.as_view(), name="tematicasUpdate"),
    path('tematicasDelete/<pk>',views.TematicaDelete.as_view(), name="tematicasDelete"),
    path('tematicasCreate',views.TematicaCreate.as_view(), name="tematicasCreate"),
    path('postRelacionados/<pk>', views.postRelacionados, name="postRelacionados"),

    path('crearTematica',views.CrearTematica, name="crearTematica"),
    path('buscarTematicas', views.buscarTematicas, name="buscarTematicas"),
    path('eliminarTematicas/<id_tematica>',views.eliminarTematicas, name="eliminarTematicas"),
    path('editarTematicas/<id_tematica>',views.editarTematicas, name= 'editarTematicas'),
    
    path('crearLenguajes', views.LenguajeCreate.as_view(), name='New'),
    #path('PostView', views.CantViewPost.as_view(), name="VistasPost")
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    
]

