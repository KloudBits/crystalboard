#encoding:utf-8
from django.forms import ModelForm
from django import forms
from principal.models import UserProfile, Lista, Comentario_Tarea, Curso, Aviso, Comentario_Aviso, Tarea, Entrega_Tarea
from django.contrib.auth.models import User
from django.forms import widgets




class ListaForm(ModelForm):
	class Meta:
		model = Lista
		exclude = ('curso')




class AvisoForm(ModelForm):
	texto = forms.CharField(error_messages={'required': 'Este campo es obligatorio'})

	class Meta:
		model = Aviso
		exclude = ('curso')

#Hay problemas en la comprensión de este form y no lo estamos usando aún
class ComentarioavisoForm(ModelForm):
	texto = forms.CharField(error_messages={'required': 'Debes escribir un comentario'})

	class Meta:
		model = Comentario_Aviso
		exclude = ('usuario','aviso')