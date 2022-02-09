from django.contrib import admin
from UserApp.models import Perfil,ComentariosPost, Avatar,Lenguaje, Likes, Post, Tematica, PostFavoritos

admin.site.register(Tematica)

admin.site.register(Lenguaje)

admin.site.register(Post)

admin.site.register(ComentariosPost)

admin.site.register(Likes)

admin.site.register(Avatar)

admin.site.register(Perfil)
admin.site.register(PostFavoritos)