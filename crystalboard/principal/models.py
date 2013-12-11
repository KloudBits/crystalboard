# encoding: utf-8
from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

############### CLASE INSTITUTO ################
class Instituto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    logo = models.ImageField(upload_to='instituto_logo')

    def __unicode__(self):
        return self.nombre
################################################


############### CLASE CURSO ####################
class Curso(models.Model):
    nombre = models.CharField(max_length=200)  # Variable que almacena el nombre del curso
    descripcion = models.TextField() #Descripción del curso
    imagen = models.ImageField(upload_to='cursos_logo')
    docente = models.OneToOneField(User)  # Variable que guarda el id del usuario (Solo puede ser DOCENTE)
    alumnos = models.ManyToManyField(User, related_name='alumnos')  #Los alumnos asignados a este curso
    instituto = models.ForeignKey(Instituto) # Instituto al cual pertenece el curso
    # Vuelve al objeto un string
    def __unicode__(self):
        return self.nombre

################################################


class Clase(models.Model):
    curso = models.ForeignKey(Curso)
    titulo = models.CharField(max_length=30)
    resumen = models.TextField(blank=True)
    stream = models.TextField(max_length=300, blank=True) #Embed de ustream, livestream o hangout
    slideshare = models.TextField(max_length=300, blank=True) #Embed de slideshare
    recursos = models.TextField(blank=True) #Texto y enlaces de dropbox (material)
    codigo = models.TextField(blank=True) #Para clases de programación

    # Vuelve al objeto un string
    def __unicode__(self):
        return self.titulo

class Infocurso(models.Model):
    curso = models.ForeignKey(Curso)
    titulo = models.CharField(max_length=200)
    texto = models.TextField()

    def __unicode__(self):
        return self.titulo

############# CLASE AVISO ######################
class Aviso(models.Model):
    curso = models.ForeignKey(Curso)  # Variable que almacena el id del curso
    texto = models.TextField()  # Variable que almacena el texto del Aviso

    # Vuelve al objeto un string
    def __unicode__(self):
        return self.texto

################################################

############# CLASE COMENTARIO_AVISO ###############
class Comentario_Aviso(models.Model):
    usuario = models.ForeignKey(User)  # Variable que almacena el id del Usuario que comenta
    texto = models.TextField()  # Variable que almacena el comentario del usuario
    aviso = models.ForeignKey(Aviso)  # Variable que almacena el id del aviso donde se esta comentando

    # Vuelve al objeto un string
    def __unicode__(self):
        return self.texto

####################################################

########### CLASE TAREA ############################
class Tarea(models.Model):
    titulo = models.CharField(max_length=30)  # Variable que almacena el nombre de la Tarea
    descripcion = models.TextField()  # Variable que almacena la descripcion de la Tarea
    fecha_registro = models.DateField(auto_now=False,
                                      auto_now_add=False)  # Variable que almacena la fecha de registro de la tarea
    fecha_limite = models.DateField(auto_now=False,
                                    auto_now_add=False)  # Variable que almacena la fecha de entrega de la tarea
    puntos = models.IntegerField(blank=True, null=True)  # Variable que almacena la calificacion de la tarea
    curso = models.ForeignKey(Curso)  # Variable que almacena el id de la Tarea

    # Vuelve al objeto un string
    def __unicode__(self):
        return self.titulo

###################################################

############## CLASE ENTREGA_TAREA ################
class Entrega_Tarea(models.Model):
    comentarios = models.TextField()  # Variable que almacena los comentarios de la tarea
    fecha = models.DateTimeField()  # Variable que almacena la fecha y hora de entrega de la tarea
    archivo = models.CharField(max_length=100)  # Variable que almacena el nombre de la tarea y su ruta
    tarea = models.ForeignKey(Tarea)  # Variable que almacena el id de la tarea
    alumno = models.ForeignKey(User)  # Variable que almacena el id del Alumno
    link_dp = models.URLField()  # Variable que almacena el link del archivo en la carpeta publica de dropbox

    # Vuelve al objeto un string
    def __unicode__(self):
        return self.archivo

###################################################

############## CLASE COMENTARIO_TAREA ################
class Comentario_Tarea(models.Model):
    usuario = models.ForeignKey(User)  # Variable que almacena el id del uasuario que comenta la tarea
    texto = models.TextField()  # Variable que almacena el comentario del usuario
    tarea = models.ForeignKey(Tarea)  # Variable que almacena el id de la tarea que se esta comentando

    # Vuelve al objeto un string
    def __unicode__(self):
        return self.texto

######################################################


#################### CLASE LISTA ###########################
class Lista(models.Model):
    clase = models.OneToOneField(Clase)  # Variable que almacena el id del curso
    fecha = models.DateField()  # Variable que almacena la fecha del pase de lista

    # Vuelve al objeto un string
    def __str__(self):
        return "%s" % self.fecha

#############################################################

###################### CLASE ASISTENCIA ########################
###Esta tabla es la que se forma de la relación muchos a muchos en la relación de lista y alumnos
class Asistencia(models.Model):
    lista = models.ForeignKey(Lista)  # Variable que almacena el id de la lista
    usuario = models.ForeignKey(User)  # Variable que almacena el id del alumno
    asis = models.BooleanField(default=False)  # Variable que almacena si asistio o no el alumno

    # Vuelve al objeto un string
    def __unicode__(self):
        return self.usuario.username

############################################################

###################### CLASE USERPROFILE ######################
class UserProfile(models.Model):
#Tipo de Perfiles existentes
    TIPO_CHOICES = (
        (1, 'DOCENTE'),
        (2, 'DIRECTOR'),
        (3, 'ALUMNO')
    )

    user = models.OneToOneField(User)
    web = models.URLField(blank=True)  # Variable que guarda la direccion web del usuario
    twitter = models.CharField(max_length=30, blank=True)  # Variable que guarda el hashtag del usuario
    facebook = models.CharField(max_length=30, blank=True)  # Variable que guarda la direccion de facebook del usuario
    bio = models.TextField(blank=True)
    foto = models.ImageField(upload_to='perfiles', blank=True)
    tipo = models.IntegerField(default=3, choices=TIPO_CHOICES)  # Variable que identifica el tipo de usuario

    instituto = models.ForeignKey(Instituto)  ## Variable que establece, a que instituto pertenece el usuario

    def __str__(self):
        return "%s's perfil" % self.user
##################################################################

class Foro(models.Model):
    fecha = models.DateField(auto_now=True)
    curso = models.ForeignKey(Curso)
    titulo = models.CharField(max_length=300)
    texto = models.TextField()

    def __unicode__(self):
        return self.titulo

### Respuestas al foro
class Respuesta(models.Model):
    fecha = models.DateField(auto_now=True)
    foro = models.ForeignKey(Foro)
    usuario = models.ForeignKey(User)
    texto = models.TextField()

    def __unicode__(self):
        return self.usuario.username

### Comentarios a las respuestas del foro
class Comentario(models.Model):
    fecha = models.DateField(auto_now=True)
    respuesta = models.ForeignKey(Respuesta)
    usuario = models.ForeignKey(User)
    texto = models.TextField()

    def __unicode__(self):
        return self.usuario.username


#########################################
## Clase prueba
#########################################
class Prueba(models.Model):
    #Nombre de la prueba
    nombre = models.CharField(max_length=150)
    fecha_creacion = models.DateTimeField()
    intentos = models.IntegerField() # intentos para presentar la prueba

##########################################
## Clase Pregunta
##########################################
class Pregunta_Prueba(models.Model):
    #Pregunta
    nombre = models.CharField(max_length=100)
    prueba = models.ForeignKey(Prueba) ## La pregunta le pertenece a la prueba x

##########################################
## Clase Respuesta
##########################################
class Respuesta_Prueba(models.Model):
    respuesta = models.CharField(max_length=100)
    correcta = models.BooleanField() ## la respuesta es correcta
    pregunta = models.ForeignKey(Pregunta_Prueba) # La respuesta le pertenece a la pregunta x

##########################################
## Clase Aplicar
##########################################
class Aplicar_Prueba(models.Model):
    usuario = models.ForeignKey(User) ### Aplicar prueba al usuario
    prueba = models.ForeignKey(Prueba) ### Que prueba se le esta aplicando
    fecha_inicio = models.DateTimeField()
    fecha_termino = models.DateTimeField()

###########################################
### Respuesta_Aplicar
###########################################
class Aplicar_Respuesta(models.Model):
    examen = models.ForeignKey(Aplicar_Prueba) ## Examen el cual se esta contestando
    pregunta = models.ForeignKey(Pregunta_Prueba) ## Pregunta a la cual se respondio
    respuesta = models.ForeignKey(Respuesta_Prueba) ## Respuesta que se eligio



