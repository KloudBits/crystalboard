#encoding:utf-8
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from Main.models import UserProfile,Curso, Clase, Capitulo, Recurso, Aviso, Aviso_Comentario, Tarea, Entrega_Tarea, Foro, Foro_Comentario, Quiz, Quiz_Pregunta, Quiz_Respuesta, Quiz_Aplicar
from django.contrib.auth.forms import UserCreationForm

class nuevoEntregaTareaFormulario(ModelForm):
	class Meta:
		model = Entrega_Tarea
		exclude = ('alumno','tarea', 'feedback',)


class nuevoCanalCursoFormulario(ModelForm):

	class Meta:
		model = Curso
		fields = ('canal','chat',)

class nuevoCursoFormulario(ModelForm):
	
	class Meta:
		model = Curso
		exclude = ('usuario', 'miembros','slug','canal', 'chat',)

class nuevaClaseFormulario(ModelForm):

	class Meta:
		model = Clase
		exclude = ('slug',)

class editarPerfilFormulario(ModelForm):
	class Meta:
		model = UserProfile
		exclude = ('user','tipo',)


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
		exclude = ('curso',)

class comentarForoFormulario(ModelForm):
	class Meta:
		model = Foro_Comentario
		fields = ('comentario',)

class nuevoForoFormulario(ModelForm):
	class Meta:
		model = Foro
		exclude = ('curso',)

#Sobre Quiz
class nuevaRespuestaFormulario(ModelForm):
	class Meta:
		model = Quiz_Respuesta
		exclude = ('pregunta','feedback', 'examen',)

class nuevaPreguntaFormulario(ModelForm):
	class Meta:
		model = Quiz_Pregunta
		exclude = ('prueba',)

class nuevoQuizFormulario(ModelForm):
	class Meta:
		model = Quiz
		exclude = ('curso','fecha_creacion',)

class nuevoRecursoFormulario(ModelForm):
	class Meta:
		model = Recurso
		exclude = ('clase', 'tipo',)

class nuevoTareaFormulario(ModelForm):
	class Meta:
		model = Tarea
		exclude = ('curso',)

#----

class registrationForm(forms.ModelForm):
	email = forms.EmailField(label="Correo electrónico", widget=forms.TextInput(attrs={'class':'form-control'}))
	password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(label="Teléfono", widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ('email', 'password1', 'password2', 'first_name', 'last_name')