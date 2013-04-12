# encoding: utf-8
from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


############### CLASE CURSO ####################
class Curso(models.Model):
	nombre = models.CharField(max_length=30) # Variable que almacena el nombre del curso
	docente = models.ForeignKey(User) # Variable que guarda el id del usuario (Solo puede ser DOCENTE)

	# Vuelve al objeto un string
	def __unicode__(self):
		return self.nombre

################################################


############# CLASE AVISO ######################
class Aviso(models.Model):
	curso = models.ForeignKey(Curso) # Variable que almacena el id del curso
	texto = models.TextField() # Variable que almacena el texto del Aviso

	# Vuelve al objeto un string
	def __unicode__(self):
		return self.curso

################################################

############# CLASE COMENTARIO_AVISO ###############
class Comentario_Aviso(models.Model):
	usuario = models.ForeignKey(User) # Variable que almacena el id del Usuario que comenta
	texto = models.TextField() # Variable que almacena el comentario del usuario
	aviso = models.ForeignKey(Aviso) # Variable que almacena el id del aviso donde se esta comentando

	# Vuelve al objeto un string
	def __unicode__(self):
		return self.texto
####################################################

########### CLASE TAREA ############################
class Tarea(models.Model):
	titulo = models.CharField(max_length=30) # Variable que almacena el nombre de la Tarea
	descripcion = models.TextField() # Variable que almacena la descripcion de la Tarea
	fecha_registro = models.DateField(auto_now = False, auto_now_add = False) # Variable que almacena la fecha de registro de la tarea
	fecha_limite = models.DateField(auto_now = False, auto_now_add = False) # Variable que almacena la fecha de entrega de la tarea
	puntos = models.IntegerField() # Variable que almacena la calificacion de la tarea
	curso = models.ForeignKey(Curso) # Variable que almacena el id de la Tarea

	# Vuelve al objeto un string
	def __unicode__(self):
		return self.titulo

###################################################

############## CLASE ENTREGA_TAREA ################
class Entrega_Tarea(models.Model):
	comentarios = models.TextField() # Variable que almacena los comentarios de la tarea
	fecha = models.DateField() # Variable que almacena la fecha de entrega de la tarea
	archivo = models.CharField(max_length=100) # Variable que almacena el nombre de la tarea y su ruta
	tarea = models.ForeignKey(Tarea) # Variable que almacena el id de la tarea

	# Vuelve al objeto un string
	def __unicode__(self):
		return self.archivo

###################################################

############## CLASE COMENTARIO_TAREA ################
class Comentario_Tarea(models.Model):
	usuario = models.ForeignKey(User) # Variable que almacena el id del uasuario que comenta la tarea
	texto = models.TextField() # Variable que almacena el comentario del usuario
	tarea = models.ForeignKey(Tarea) # Variable que almacena el id de la tarea que se esta comentando

	# Vuelve al objeto un string
	def __unicode__(self):
		return self.texto

######################################################


#################### CLASE LISTA ###########################
class Lista(models.Model):
	curso = models.ForeignKey(Curso) # Variable que almacena el id del curso
	usuario = models.ForeignKey(User) # Variable que almacena el id del alumno
	fecha = models.DateField() # Variable que almacena la fecha del pase de lista
	asistencia = models.BooleanField() # Variable que almacena si el alumno asistio o no

	# Vuelve al objeto un string
	def __unicode__(self):
		return self.fecha

############################################################


class UserProfile(models.Model):
	TIPO_CHOICES = (
		(1, 'DOCENTE'),
		(2, 'DIRECTOR'),
		(3, 'ALUMNO')
	)
	user = models.OneToOneField(User)
	nombre = models.CharField(max_length=100) # Variable que guarda el nombre del usuario
	usuario = models.CharField(max_length=16) # Variable que guarda el nickname del usuario
	password = models.CharField(max_length=20) # Variable que guarda la contraseña del usuario
	web = models.CharField(max_length=30) # Variable que guarda la direccion web del usuario
	twitter = models.CharField(max_length=30) # Variable que guarda el hashtag del usuario
	facebook = models.CharField(max_length=30) # Variable que guarda la direccion de facebook del usuario
	tipo = models.IntegerField(default=3, choices=TIPO_CHOICES) # Variable que identifica el tipo de usuario

	def __str__(self):  
		return "%s's perfil" % self.user 