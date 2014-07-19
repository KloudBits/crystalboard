#encoding:utf-8
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from models import Curso, Clase, Capitulo, Recurso, Aviso, Aviso_Comentario, Tarea, Entrega_Tarea, Foro, Foro_Comentario, Quiz, Quiz_Pregunta, Quiz_Respuesta, Quiz_Aplicar, Aplicar_Respuesta
from django.contrib.auth.forms import UserCreationForm

class nuevoCurso(ModelForm):
	colonia = forms.ModelChoiceField(label="Colonia", queryset=Colonia.objects.all(),widget=forms.Select(attrs={'class':'formDropdown'}), empty_label='Cualquiera')
	
	class Meta:
		model = Curso
		exclude = ('usuario', 'miembros',)
