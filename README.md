# ProyectoGrupo6
#Carga el inicio con un usuario, cerrar sesion, probar el registro
#iniciar sesion
#Apretar en "Leer mas" para ver el posteo en cuestion
#Comentarlo
#crear post*
#buscar tematicas en la barra lateral



*Cuando creo el post y selecciono la o las tematicas no me las carga... en el admin aparecen como que no se seleccionó ninguna
##No se cargan por esta linea:

-->post.save(commit=False)

post.posteador=req.user
post.save()

#La idea seria que se detecte automaticamente qué usuario está escribiendo el Post y restringir que si un usuario no está registrado no pueda crear un post
