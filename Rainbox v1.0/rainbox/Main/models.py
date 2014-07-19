# encoding: utf-8

####################################
####  Ultima edición 7-19-2014  ####
####################################

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


import datetime


################## CURSO ########################
class Curso( models.Model ):
    nombre = models.CharField( max_length = 200 ) # Variable que almacena el nombre del curso
    slug = models.SlugField()
    resumen = models.CharField( max_length = 300 ) # Resumen corto del curso
    informacion_general = models.TextField( ) # Informacion en general del curso, temario, objetivos
    imagen = models.ImageField( upload_to = 'cursos_logo' ) # Imagen del Curso
    usuario = models.OneToOneField( User )  # Usuario que administra el curso
    miembros = models.ManyToManyField( User, related_name = 'miembros' )  # Los miembros del curso

    def __unicode__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if self.nombre:
            self.slug = slugify(self.nombre)


        super(Curso, self).save(*args, **kwargs)
################################################   

################## CAPITULO ####################
class Capitulo( models.Model ):
    curso = models.ForeignKey( Curso ) # ID del curso al que pertenece
    nombre = models.CharField( max_length = 30 ) # Nombre del capitulo
    resumen = models.TextField( blank = True ) # Información del Capítulo

    def __unicode__( self ):
        return self.nombre
################################################

#################### CLASE #####################
class Clase( models.Model ):
    capitulo = models.ForeignKey( Capitulo ) # ID del capitulo al que pertenece la clase
    titulo = models.CharField( max_length = 30 ) # Título de la clase
    resumen = models.TextField( blank = True ) # Información del curso
    
    def __unicode__( self ):
        return self.titulo
################################################

################# Recurso ######################
class Recurso( models.Model ):
    # Tipo de Perfiles existentes
    TIPO_CHOICES = (
        ( 1, 'Slideshare' ),
        ( 2, 'Dropbox' ),
        ( 3, 'Stream' ),
        ( 2, 'Youtube' ),
    )
    clase = models.ForeignKey( Clase ) # ID de la clase a la que pertenece la tarea
    titulo = models.CharField( max_length = 60 ) # Titulo del recurso
    url = models.URLField( ) # URL de ubicación web
    descripcion = models.TextField( ) # Resumen del contenido del recurso
    tipo = models.IntegerField( default = 2, choices = TIPO_CHOICES ) # Tipo de recurso que se va agregar
################################################

################### AVISO ######################
class Aviso( models.Model ):
    curso = models.ForeignKey( Curso ) # ID del Curso al que pertenece el Aviso
    titulo = models.CharField( max_length = 30 ) # Titulo del aviso
    texto = models.TextField( ) # Información del Aviso

    def __unicode__( self ):
        return self.texto
################################################

############### COMENTARIO AVISO ###############
class Aviso_Comentario( models.Model ):
    aviso = models.ForeignKey( Aviso ) # Aviso donde se hace el comentario
    usuario = models.ForeignKey( User ) # ID usuario que comenta el aviso
    texto = models.TextField( ) # Comentario del usuario    

    def __unicode__( self ):
        return self.texto
################################################

################# TAREA ########################
class Tarea( models.Model ):
    clase = models.ForeignKey( Clase ) # ID de la clase a la que pertenece la tarea
    titulo = models.CharField( max_length = 30 ) # Título de la Tarea
    descripcion = models.TextField( blank = True, null = True ) # Texto informativo sobre la tarea
    fecha_registro = models.DateField( auto_now = True, auto_now_add = True ) # Fecha en la que se registo la fecha
    fecha_inicio = models.DateField( auto_now = False, auto_now_add = True ) # Fecha en la que se abre el acceso
    fecha_limite = models.DateField( auto_now = False, auto_now_add = False) # Fecha limite de entrega la materia
    puntos = models.IntegerField( blank = True, null = True ) # Puntos que otorga la tarea
    
    def __unicode__( self ):
        return self.titulo
################################################

################# ENTREGA TAREA ################
class Entrega_Tarea( models.Model ):
    tarea = models.ForeignKey( Tarea ) # ID de la tarea que se entrega
    alumno = models.ForeignKey( User ) # ID del alumno que entrega la tarea
    comentarios = models.TextField( blank = True ) # Comentarios del alumno sobre la tarea
    fecha = models.DateTimeField( auto_now = True, auto_now_add = True ) # Feha y hora de la entrega    
    link_dp = models.URLField( ) # Link de dropbox para compartir la tarea

    def __unicode__( self ):
        return self.link_dp
#################################################

################# USERPROFILE ###################
class UserProfile( models.Model ):
    # Tipo de Perfiles existentes
    TIPO_CHOICES = (
        ( 1, 'Usuario' ),
        ( 2, 'Miembro' ),
    )
    user = models.OneToOneField( User ) # ID del usuario de Django
    web = models.URLField( blank = True ) # Página Web del usuario
    twitter = models.CharField( max_length = 30, blank = True ) # Cuenta de twitter
    facebook = models.CharField(max_length = 30, blank = True ) # Cuenta de facebook
    bio = models.TextField( blank = True ) # Pequeña biografía del usuaria
    foto = models.ImageField( upload_to = 'perfiles', blank = True ) # foto que se muestra
    tipo = models.IntegerField( default = 1, choices = TIPO_CHOICES ) # Tipo de perfil del usuario
    
    def __str__( self ):
        return "%s's perfil" % self.user
#################################################

#################### FORO #######################
class Foro( models.Model ):
    curso = models.ForeignKey( Curso ) # ID del curso al que pertenece
    fecha = models.DateField( auto_now = True, auto_now_add = True ) # Fecha en la que el foro es creado
    titulo = models.TextField( max_length = 30 ) # Titulo del foro
    texto = models.TextField( ) # Descripción del foro
    visibilidad = models.BooleanField() # Opción de visibilidad

    def __unicode__( self ):
        return self.titulo
#################################################

############ COMENTARIO DEL FORO ################
class Foro_Comentario( models.Model ):
    foro = models.ForeignKey( Foro ) # ID del Foro que fue comentado 
    usuario = models.ForeignKey( User ) # ID del usuario que comento
    fecha = models.DateField( auto_now = True, auto_now_add = True ) # Fecha en la que fue creado el comentado  
    comentario = models.TextField( ) # Texto del comentario

    def __unicode__( self ):
        return self.comentario
#################################################

################## QUIZ  ########################
class Quiz( models.Model ):
    curso = models.ForeignKey( Curso ) # A que curso pertenece
    nombre = models.CharField( max_length = 150 ) # Nombre del quiz
    fecha_creacion = models.DateTimeField( auto_now = True, auto_now_add = True ) # Fecha en la que se creo el quiz
    fecha_inicio = models.DateTimeField( ) # Fecha en la que se muestra el quiz
    fecha_limite = models.DateTimeField( ) # Fecha Limite de acceso
    intentos = models.IntegerField( ) # Intentos para presentar el quiz

    def __unicode__( self ):
        return self.nombre
################################################

################ QUIZ_PREGUNTA  ################
class Quiz_Pregunta( models.Model ):    
    prueba = models.ForeignKey( Quiz ) # La pregunta le pertenece a la prueba x
    nombre_pregunta = models.CharField( max_length = 100 ) # La Pregunta    

    def obtener_respuestas( self ):
        return Quiz_Respuesta.objects.filter( pregunta = self.pk ) # Obtener todas las respuestas ha esta pregunta

    def __unicode__( self ):
        return self.nombre_pregunta
################################################

############## QUIZ_RESPUESTA ##################
class Quiz_Respuesta( models.Model ):
    pregunta = models.ForeignKey( Quiz_Pregunta ) # La pregunta a la que pertenece la respuesta
    respuesta = models.CharField( max_length = 100 ) # Opción de la pregunta
    correcta = models.BooleanField( ) # es la respuesta es correcta
    
    def __unicode__( self ):
        return self.respuesta
################################################

############### QUIZ_Aplicar ###################
class Quiz_Aplicar( models.Model ):
    usuario = models.ForeignKey( User ) # Usuario al que se le aplica el quiz
    quiz = models.ForeignKey( Quiz ) # Quiz que se va a aplicar
    intento = models.IntegerField( ) # Intentos que lleva de realizar el quiz
    fecha_inicio = models.DateTimeField( ) # Hora de Inicio del quiz
    fecha_termino = models.DateTimeField( ) # Hora de Termino del quiz
#################################################

############ APLICAR_RESPUESTA ##################
class Aplicar_Respuesta( models.Model ):
    examen = models.ForeignKey( Quiz_Aplicar ) # Quiz que se esta contestando
    pregunta = models.ForeignKey( Quiz_Pregunta ) # Pregunta que se contesta
    respuesta = models.ForeignKey( Quiz_Respuesta ) # Respuesta seleccionada
#################################################