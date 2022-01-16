import email
from socket import fromshare
from UserApp.models import Post, Tematica
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    #Por qué no ponemos username=forms.text...?
    email= forms.EmailField()
    password1= forms.CharField(label='Contraseña', widget= forms.PasswordInput)
    password2=forms.CharField(label='Repetir contraseña', widget= forms.PasswordInput)

    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2']
        help_texts= {k:"" for k in fields}



class PostForm(forms.ModelForm):
    
    class Meta:  
        model=Post
        fields = ('titulo','contenido','tematica')
        label={
            'titulo': 'Titulo del posteo',
            'contenido': 'Contenido',
            'tematica':'Tematica',
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
            )
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
    