from django.contrib import admin
from UserApp.models import ComentariosPost, Lenguaje, Likes, Post, Tematica

admin.site.register(Tematica)

admin.site.register(Lenguaje)

admin.site.register(Post)

admin.site.register(ComentariosPost)

admin.site.register(Likes)