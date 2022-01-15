from django.urls import path
from UserApp import views
urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('padre', views.padre, name="padre"),
    path('iniciarSesion/', views.Login, name="inicioSesion"),
    path('Posteos', views.verPosteos, name="Posteos"),
    #path('PostView', views.CantViewPost.as_view(), name="VistasPost")
]
