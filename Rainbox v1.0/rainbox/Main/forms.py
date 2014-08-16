#encoding:utf-8
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from Main.models import UserProfile,Curso, Clase, Capitulo, Recurso, Aviso, Aviso_Comentario, Tarea, Entrega_Tarea, Foro, Foro_Comentario, Quiz, Quiz_Pregunta, Quiz_Respuesta, Quiz_Aplicar, Aplicar_Respuesta
from django.contrib.auth.forms import UserCreationForm

class nuevoCursoFormulario(ModelForm):
	
	class Meta:
		model = Curso
		exclude = ('usuario', 'miembros','slug',)

class nuevaClaseFormulario(ModelForm):

	class Meta:
		model = Clase
		exclude = ('slug',)

class editarPerfilFormulario(ModelForm):
	class Meta:
		model = UserProfile

class nuevoCapituloFormulario(ModelForm):
	class Meta:
		model = Capitulo
		exclude = ('curso',)

class nuevoForoFormulario(ModelForm):
	class Meta:
		model = Foro


class nuevoAvisoFormulario(ModelForm):
	class Meta:
		model = Aviso