# encoding: utf-8

####################################
####  Ultima edición 25-03-2015 ####
####################################

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

import datetime


################## CURSO ########################
class Curso( models.Model ):
    usuario = models.ForeignKey( User )  # Usuario que administra el curso
    nombre = models.CharField( max_length = 200 ) # Variable que almacena el nombre del curso
    slug = models.SlugField()
    informacion_general = models.TextField( ) # Informacion en general del curso, temario, objetivos
    imagen = models.ImageField( upload_to = 'cursos_logo' ) # Imagen del Curso    
    canal = models.CharField(blank=True, max_length=100) # URL del canal de streaming
    chat = models.CharField(max_length=100, blank=True)
    miembros = models.ManyToManyField(User, related_name = 'miembros', blank=True )  # Los miembros del curso

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
    nombre = models.CharField( max_length = 100 ) # Nombre del capitulo
    resumen = models.TextField( blank = True ) # Información del Capítulo

    def __unicode__( self ):
        return self.nombre
################################################

#################### CLASE #####################
class Clase( models.Model ):
    capitulo = models.ForeignKey( Capitulo, verbose_name=u"Módulo" ) # ID del capitulo al que pertenece la clase
    titulo = models.CharField( max_length = 100 ) # Título de la clase
    resumen = models.TextField( blank = True ) # Información del curso
    slug = models.SlugField( )
    fecha_inicio = models.DateField() # Fecha en la que se abre el acceso
    fecha_limite = models.DateField() # Fecha limite de entrega la materia
    
    def __unicode__( self ):
        return self.titulo

    def save( self, *args, **kwargs):
        if self.titulo:
            self.slug = slugify(self.titulo)
        super(Clase, self).save(*args, **kwargs)

################################################

################# Recurso ######################
class Recurso( models.Model ):
    # Tipo de Perfiles existentes
    TIPO_CHOICES = (
        ( 1, 'Slideshare' ),
        ( 2, 'Dropbox' ),
        ( 3, 'Youtube' ),
        ( 4, 'Weblink')
    )
    clase = models.ForeignKey( Clase ) # ID de la clase a la que pertenece la tarea
    titulo = models.CharField( max_length = 100 ) # Titulo del recurso
    url = models.CharField( max_length = 200 ) # URL de ubicación web    
    descripcion = models.TextField(blank=True,null=True) # Resumen del contenido del recurso
    tipo = models.IntegerField( default = 2, choices = TIPO_CHOICES ) # Tipo de recurso que se va agregar
    
################################################

################### AVISO ######################
class Aviso( models.Model ):
    fecha = models.DateField(auto_now=True)
    curso = models.ForeignKey( Curso ) # ID del Curso al que pertenece el Aviso
    titulo = models.CharField( max_length = 100 ) # Titulo del aviso
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
    curso = models.ForeignKey( Curso ) # ID de la clase a la que pertenece la tarea
    titulo = models.CharField( max_length = 300 ) # Título de la Tarea
    descripcion = models.TextField( blank = True, null = True ) # Texto informativo sobre la tarea
    link_dp = models.URLField(blank = True, null = True) # Link de dropbox para compartir la tarea
    fecha_registro = models.DateField( auto_now = True, auto_now_add = True ) # Fecha en la que se registo la fecha
    fecha_inicio = models.DateField() # Fecha en la que se abre el acceso
    fecha_limite = models.DateField() # Fecha limite de entrega la materia
    #puntos = models.IntegerField( blank = True, null = True ) # Puntos que otorga la tarea
    
    def __unicode__( self ):
        return self.titulo
################################################

################# ENTREGA TAREA ################
class Entrega_Tarea( models.Model ):
    tarea = models.ForeignKey( Tarea ) # ID de la tarea que se entrega
    alumno = models.ForeignKey( User ) # ID del alumno que entrega la tarea
    comentarios = models.TextField( blank = True ) # Comentarios del alumno sobre la tarea
    fecha = models.DateTimeField( auto_now = True, auto_now_add = True ) # Feha y hora de la entrega    
    link_dp = models.URLField(blank = True, null = True) # Link de dropbox para compartir la tarea
    feedback  = models.TextField(blank=True)
    calificacion = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)

    def __unicode__( self ):
        return self.link_dp

    def tieneFeedback(self):
        return len(self.feedback) > 0
#################################################

################# USERPROFILE ###################
class UserProfile( models.Model ):
    # Tipo de Perfiles existentes
    TIPO_CHOICES = (
        ( 1, 'Usuario' ),
        ( 2, 'Miembro' ),
    )
    user = models.OneToOneField( User ) # ID del usuario de Django
    web = models.URLField( blank = True, null=True ) # Página Web del usuario
    twitter = models.CharField( max_length = 100, blank = True, null=True ) # Cuenta de twitter
    facebook = models.CharField(max_length = 100, blank = True, null=True ) # Cuenta de facebook
    bio = models.TextField( blank = True ) # Pequeña biografía del usuaria
    foto = models.ImageField( upload_to = 'perfiles', blank = True, null=True ) # foto que se muestra
    tipo = models.IntegerField( default = 1, choices = TIPO_CHOICES ) # Tipo de perfil del usuario
    
    def __str__( self ):
        return "%s's perfil" % self.user
#################################################

#################### PREGUNTA ###################
class Pregunta(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    curso = models.ForeignKey(Curso)
    creador = models.ForeignKey(User)
    titulo = models.CharField(max_length=300)
    descripcion = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.titulo
#################################################

############ COMENTARIO DE LA PREGUNTA ################
class Pregunta_Comentario( models.Model ):
    pregunta = models.ForeignKey( Pregunta ) # ID del Foro que fue comentado 
    usuario = models.ForeignKey( User ) # ID del usuario que comento
    fecha = models.DateTimeField( auto_now = True, auto_now_add = True ) # Fecha en la que fue creado el comentado  
    comentario = models.TextField( ) # Texto del comentario

    def __unicode__( self ):
        return self.comentario
#################################################

#################### FORO #######################
class Foro( models.Model ):
    curso = models.ForeignKey( Curso ) # ID del curso al que pertenece
    fecha = models.DateField( auto_now = True, auto_now_add = True ) # Fecha en la que el foro es creado
    titulo = models.CharField( max_length = 100 ) # Titulo del foro
    texto = models.TextField( ) # Descripción del foro
    fecha_inicio = models.DateTimeField( ) # Fecha en la que se muestra el foro
    fecha_limite = models.DateTimeField( ) # Fecha Limite de acceso

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
    nombre = models.CharField( max_length = 300 ) # Nombre del quiz
    fecha_creacion = models.DateTimeField( auto_now = True, auto_now_add = True ) # Fecha en la que se creo el quiz
    fecha_inicio = models.DateTimeField( ) # Fecha en la que se muestra el quiz
    fecha_limite = models.DateTimeField( ) # Fecha Limite de acceso
    #intentos = models.IntegerField( ) # Intentos para presentar el quiz

    def __unicode__( self ):
        return self.nombre
################################################

################ QUIZ_PREGUNTA DE TEXTO  ################
class Quiz_Pregunta( models.Model ):    
    prueba = models.ForeignKey( Quiz ) # La pregunta le pertenece a la prueba x
    nombre_pregunta = models.CharField( max_length = 300 ) # La Pregunta   

    def obtener_respuestas( self ):
        return Quiz_Respuesta.objects.filter( pregunta = self.pk ) # Obtener todas las respuestas ha esta pregunta

    def __unicode__( self ):
        return self.nombre_pregunta
################################################


# ############## QUIZ_RESPUESTA_OPCION ##################
class Quiz_Respuesta(models.Model ):
    pregunta = models.ForeignKey( Quiz_Pregunta ) # La pregunta a la que pertenece la respuesta
    respuesta = models.CharField( max_length = 300 ) # Opción de la pregunta
    correcta = models.BooleanField( ) # es la respuesta es correcta
    
    def __unicode__( self ):
        return self.respuesta
# ################################################

############### QUIZ_Aplicar ###################
class Quiz_Aplicar( models.Model ):
    usuario = models.ForeignKey( User ) # Usuario al que se le aplica el quiz
    quiz = models.ForeignKey( Quiz ) # Quiz que se va a aplicar
    #intento = models.IntegerField( ) # Intentos que lleva de realizar el quiz
    fecha_inicio = models.DateTimeField( ) # Hora de Inicio del quiz
    fecha_termino = models.DateTimeField( ) # Hora de Termino del quiz

    def __unicode__(self):
        return str(self.quiz) + " de " + str(self.usuario)
################################################

# ############ APLICAR_RESPUESTA ##################
class Aplicar_Respuesta( models.Model ):
    examen = models.ForeignKey( Quiz_Aplicar ) # Quiz que se esta contestando
    pregunta = models.ForeignKey( Quiz_Pregunta ) # Pregunta que se contesta
    respuesta = models.ForeignKey( Quiz_Respuesta ) # Respuesta seleccionada
# #################################################
