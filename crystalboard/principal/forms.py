#encoding:utf-8
from django.forms import ModelForm
from django.forms.widgets import RadioSelect
from django import forms
from principal.models import Respuesta_Prueba, Pregunta_Prueba, Prueba, Comentario, Respuesta, Foro, Clase, Infocurso, UserProfile, Lista, Comentario_Tarea, Curso, Aviso, Comentario_Aviso, Tarea, Entrega_Tarea
from django.contrib.auth.models import User
from django.forms import widgets
from django.core.exceptions import ValidationError ### libreria para validar datos
import datetime

class NuevoCursoFormulario(ModelForm):
    class Meta:
        model = Curso
        exclude = ('instituto', )

class ClaseEditarFormulario(ModelForm):
	class Meta:
		model = Clase
		exclude = ('clase','curso', 'titulo', )

class InfocursoForm(ModelForm):
	class Meta:
		model = Infocurso
		exclude = ('curso',)

class EntregaForm(ModelForm):
	class Meta:
		model = Entrega_Tarea
		exclude = ('fecha', 'tarea', 'alumno', )

class TareaForm(ModelForm):
	fecha_limite = forms.DateField(initial=datetime.date.today())
	class Meta:
		model = Tarea
		exclude = ('fecha_registro', 'puntos', 'curso', )

class AvisoForm(ModelForm):
	texto = forms.CharField(label="Aviso", widget=forms.Textarea ,error_messages={'required': 'Este campo es obligatorio'})

	class Meta:
		model = Aviso
		exclude = ('curso', )

class ForoForm(ModelForm):
    class Meta:
        model = Foro
        exclude = ('curso', )
    
#Hay problemas en la comprensión de este form y no lo estamos usando aún
class ComentarioavisoForm(ModelForm):
	texto = forms.CharField(error_messages={'required': 'Debes escribir un comentario'})

	class Meta:
		model = Comentario_Aviso
		exclude = ('usuario','aviso', )

class RespuestaForm(ModelForm):
	class Meta:
		model = Respuesta
		exclude = ('foro','usuario', )

class ComentarioForm(ModelForm):
	class Meta:
		model = Comentario
		exclude = ('respuesta', 'usuario', )

class ClaseForm(ModelForm):
	class Meta:
		model = Clase
		exclude = ('curso', )

###################################
########## LO NUEVO ##############
#################################

class PruebaForm(ModelForm):
    class Meta:
        model = Prueba
        exclude = ('curso', 'fecha_creacion', )

class Pregunta_PruebaForm(ModelForm):
    class Meta:
        model = Pregunta_Prueba
        exclude = ('prueba', )

class Respuesta_PruebaForm(ModelForm):
    class Meta:
        model = Respuesta_Prueba
        exclude = ('pregunta', )