import email
from mimetypes import init
from re import S
from UserApp.models import Post, Tematica, ComentariosPost,Perfil
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class PostFormulario(forms.Form):   
    titulo              = forms.CharField(max_length=100)
    contenido           = forms.CharField(max_length=100000000)
    tematica            = forms.CharField(max_length=100)

class UserRegisterForm(UserCreationForm):
    #Por qué no ponemos username=forms.text...?
    email= forms.EmailField()
    password1= forms.CharField(label = 'Contraseña', widget= forms.PasswordInput)
    password2=forms.CharField(label = 'Repetir contraseña', widget= forms.PasswordInput)
    biografia=forms.CharField(label = 'Quien es usted?')

    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2', 'biografia']
        help_texts= {k:"" for k in fields}

class UserEditForm(UserCreationForm):
    email= forms.EmailField()
    password1= forms.CharField(label='Contraseña', widget= forms.PasswordInput)
    password2=forms.CharField(label='Repetir contraseña', widget= forms.PasswordInput)
    # first_name= forms.CharField()
    # last_name= forms.CharField()
    class Meta:
        model = User
        fields = ['email','password1', 'password2']
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['imagenPerfil', 'biografia']
class PostForm(forms.ModelForm):
    # def __init__(self,*args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     self.fields['imagenPost'].required=False
    class Meta:  
        model=Post
        fields = ('titulo','contenido','tematica','imagenPost')
        label={
            'titulo': 'Titulo del posteo',
            'contenido': 'Contenido',
            'tematica':'Tematica',
            'imagenPost': 'Imagen', 
        }
        widgets = {
            'titulo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el titulo del posteo'
                }
            ),
            'contenido': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Desahoguese...'
                }
            ),
            'tematica': forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                    
                }
            ),
            'imagenPost': forms.FileInput(
                attrs={
                    'required':False
                    # 'class': 'form-control'
                }
            )
            # 'imagen' : forms.ImageField(
            #     attrs={
            #         'class' : 'form-control'
            #     }
            # )
            
            }
 
#me muestra las tematicas disponibles cuando creo el Post, sin embargo no lo veo reflejado en la base de datossss


class TematicaForm(forms.ModelForm):
    class Meta:
        model=Tematica
        fields=('nombre',)
        label={
            'nombre': 'Nombre de la tematica'
        }
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la tematica...'
                }
            )
        }
    
class LenguajeFormulario(forms.Form):
    nombreLenguaje= forms.CharField()

class ComentarioForm(forms.ModelForm):
    class Meta:
        model=ComentariosPost
        fields=('contenido_comentario',)
        label={
            'contenido_comentario': 'Comentario'
        }
        widgets = {
            'contenido_comentario':forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Desahoguese...'
                }
            )
        }
class AvatarFormulario(forms.Form):

    #Especificar los campos
    
    imagen = forms.ImageField(required=False)