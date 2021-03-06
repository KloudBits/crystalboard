#encoding:utf-8
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from Main.models import Pregunta, Pregunta_Comentario, UserProfile,Curso, Clase, Capitulo, Recurso, Aviso, Aviso_Comentario, Tarea, Entrega_Tarea, Foro, Foro_Comentario, Quiz, Quiz_Pregunta, Quiz_Respuesta, Quiz_Aplicar
from django.contrib.auth.forms import UserCreationForm

class nuevoEntregaTareaFormulario(ModelForm):
	comentarios = forms.CharField(required=False,label="Recuadro de respuesta o comentarios:", widget=forms.Textarea(attrs={'class':'form-control'}))
	link_dp = forms.CharField(required=False, label="Enlace de dropbox")
	class Meta:
		model = Entrega_Tarea
		exclude = ('alumno','tarea', 'feedback', 'calificacion', )


class nuevoCanalCursoFormulario(ModelForm):

	class Meta:
		model = Curso
		fields = ('canal','chat',)

class nuevoCursoFormulario(ModelForm):
	
	class Meta:
		model = Curso
		exclude = ('usuario', 'miembros','slug','canal', 'chat',)

class nuevaClaseFormulario(ModelForm):
	fecha_inicio = forms.CharField(widget=forms.TextInput(attrs={'class':'fechado'}))
	fecha_limite = forms.CharField(widget=forms.TextInput(attrs={'class':'fechado'}))
	class Meta:
		model = Clase
		exclude = ('slug',)

class editarPerfilFormulario(ModelForm):
	web = forms.CharField(required=False,label="Página web", widget=forms.TextInput(attrs={'class':'form-control'}))
	bio = forms.CharField(required=False,label="Biografía personal", widget=forms.Textarea(attrs={'class':'form-control'}))

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

class nuevoPreguntaFormulario(ModelForm):
	class Meta:
		model = Pregunta
		exclude = ('creador', 'curso',)

class comentarPreguntaFormulario(ModelForm):
	comentario = forms.CharField(required=True,label="Comentar:", widget=forms.Textarea(attrs={'class':'form-control'}))
	class Meta:
		model = Pregunta_Comentario
		fields = ('comentario',)


class nuevoAvisoFormulario(ModelForm):
	class Meta:
		model = Aviso
		exclude = ('curso',)

class comentarForoFormulario(ModelForm):
	comentario = forms.CharField(required=True,label="Tu participación en este foro:", widget=forms.Textarea(attrs={'class':'form-control'}))
	class Meta:
		model = Foro_Comentario
		fields = ('comentario',)

class nuevoForoFormulario(ModelForm):
	fecha_inicio = forms.CharField(widget=forms.TextInput(attrs={'class':'fechado'}))
	fecha_limite = forms.CharField(widget=forms.TextInput(attrs={'class':'fechado'}))
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
	fecha_inicio = forms.CharField(widget=forms.TextInput(attrs={'class':'fechado'}))
	fecha_limite = forms.CharField(widget=forms.TextInput(attrs={'class':'fechado'}))
	class Meta:
		model = Quiz
		exclude = ('curso','fecha_creacion',)

class nuevoRecursoFormulario(ModelForm):
	url = forms.CharField(label="Enlace de recurso", widget=forms.TextInput(attrs={'class':'form-control'}))
	class Meta:
		model = Recurso
		exclude = ('clase', 'tipo',)

class nuevoTareaFormulario(ModelForm):
	fecha_inicio = forms.CharField(widget=forms.TextInput(attrs={'class':'fechado'}))
	fecha_limite = forms.CharField(widget=forms.TextInput(attrs={'class':'fechado'}))
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