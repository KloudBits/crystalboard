#encoding:utf-8

####################################
#### Ultima edición 7/19/2014   ####
####################################

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Avg, Count
from django.template.defaultfilters import slugify
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from Main.models import Entrega_Tarea, Quiz_Aplicar, Quiz_Respuesta, Quiz_Pregunta, Quiz, UserProfile, Curso, Tarea, Clase, Recurso, Capitulo, Foro, Foro_Comentario, Aviso
from Main.forms import nuevoEntregaTareaFormulario, nuevoTareaFormulario, nuevoRecursoFormulario, nuevaRespuestaFormulario, nuevaPreguntaFormulario, nuevoQuizFormulario, comentarForoFormulario, nuevoCursoFormulario, nuevaClaseFormulario, nuevoCapituloFormulario, nuevoForoFormulario, nuevoAvisoFormulario, registrationForm, editarPerfilFormulario, nuevoCanalCursoFormulario
import urllib
import json
import datetime
from django import forms

########################## LOGEO #######################################
def ingreso_usuario( request ):
	if request.method == 'POST':
		formulario = AuthenticationForm( request.POST )
		if formulario.is_valid:
			usuario = request.POST [ 'username' ]
			clave = request.POST [ 'password' ]
			acceso = authenticate( username = usuario, password = clave )
			if acceso is not None:
				login( request, acceso )
				return HttpResponseRedirect( '/' )
			else:
				messages.add_message( request, messages.ERROR, 'El usuario o contraseña son incorrectos' )
				return HttpResponseRedirect( '/login/' )
	else: 
		if not request.user.is_authenticated( ):
			formulario = AuthenticationForm( )
		else:
			return HttpResponseRedirect( '/' )
	return render( request, 'login.html', { 'formulario' : formulario } )

def egreso_usuario( request ):
	logout( request )
	return HttpResponseRedirect( '/login/' )
#########################################################################

############################## Home  ####################################
def home( request ):
	if not request.user.is_authenticated( ):
		return render(request, 'index.html')
	else: 
		perfil = UserProfile.objects.get( user = request.user )
		if perfil.tipo == 1: # Tipo de perfil Usuario ( Admin ) 
			cursos = Curso.objects.filter( usuario = request.user )
			template = "usuarios/home.html"
		elif perfil.tipo == 2: # Tipo de perfil miembro ( Consumidor )
			cursos = Curso.objects.filter( miembros = request.user )
			template = "miembros/home.html"
		return render( request, template, { 'cursos' : cursos } )
#########################################################################

######################## Perfil Usuario #################################
def perfil( request ):
	if not request.user.is_authenticated( ):
		raise Http404
	else:
		perfil = UserProfile.objects.get( user = request.user )
		if request.method == "POST":
			formulario = editarPerfilFormulario( request.POST, instance = perfil )
			if formulario.is_valid( ):
				formulario.save( )
				messages.add_message( request, messages.SUCCESS, "Se editó correctamente")
		else:
			formulario = editarPerfilFormulario( instance = perfil )
		return render( request, "usuarios/perfil.html", { 'perfil' : perfil, 'formulario' : formulario } )
#########################################################################

########################    Cursos      #################################
def cursos( request ):
	if not request.user.is_authenticated( ):
		raise Http404
	else:
		perfil = UserProfile.objects.get( user = request.user )		
		if perfil.tipo == 1: # Tipo de perfil usuario ( Admin )
			cursos = Curso.objects.filter( usuario = request.user )
			template = "usuarios/cursos.html"
		elif perfil.tipo == 2: # Tipo de perfil miembro ( Consumidor )
			cursos = Curso.objects.filter( miembros = request.user )
			template = "miembros/cursos.html"
		return render( request, template, { "cursos" : cursos } )
#########################################################################

###########################    Curso    #################################
def curso( request, curso ):
	if not request.user.is_authenticated( ):
		raise Http404
	else:
		clases = Clase.objects.filter(capitulo__curso__slug = curso )
		perfil = UserProfile.objects.get( user = request.user )
		if perfil.tipo == 1: # Tipo de perfil de usuario ( Admin )
			template = "usuarios/curso.html"
		elif perfil.tipo == 2: # Tipo de perfil miembro ( Consumidor )
			template = "miembros/curso.html"
		return render( request, template, { "clases" : clases, "curso" : get_object_or_404(Curso, slug = curso) } )
################ CRUD ##################
def nuevoCurso( request ):
	if not request.user.is_authenticated( ):
		raise Http404
	else: 
		perfil = UserProfile.objects.get( user = request.user )
		if perfil.tipo != 1:
			raise Http404
		else:
			if request.method == "POST":
				formulario = nuevoCursoFormulario( request.POST, request.FILES )
				if formulario.is_valid( ) and formulario.is_multipart( ):
					nuevo_curso = formulario.save( commit = False )
					nuevo_curso.usuario = request.user
					nuevo_curso.save( )
					messages.add_message( request, messages.SUCCESS, 'Registro de curso exitoso' )
					return HttpResponseRedirect( '/' )
			else:

				formulario = nuevoCursoFormulario( )
	return render( request, 'usuarios/nuevoCurso.html', { "formulario" : formulario } )

def editarCurso( request, curso ):
	if not request.user.is_authenticated( ):
		raise Http404
	else: 
		perfil = UserProfile.objects.get( user = request.user )
		if perfil.tipo != 1:
			raise Http404
		else:
			curso = get_object_or_404( Curso, pk = curso )
			if request.method == "POST":
				formulario = nuevoCursoFormulario( request.POST, instance = curso )
				if formulario.is_valid( ):
					formulario.save( )
					messages.add_message( request, messages.SUCCESS, "Se editó correctamente" )
			else:
				formulario = nuevoCursoFormulario( instance = curso )
			return render( request, 'usuarios/nuevoCurso.html', { "formulario" : formulario } )	
#########################################################################

###########################    Curso    #################################
def clases( request, curso ):
	if not request.user.is_authenticated( ):
		raise Http404
	else:
		curso = get_object_or_404(Curso, slug=curso)
		clases = Clase.objects.filter(capitulo__curso = curso )
		perfil = UserProfile.objects.get( user = request.user )
		if perfil.tipo == 1: # Tipo de perfil de usuario ( Admin )
			template = "usuarios/clases.html"
		elif perfil.tipo == 2: # Tipo de perfil miembro ( Consumidor )
			template = "miembros/clases.html"
		return render( request, template, { "clases" : clases, "curso":curso } )

###############################  Clase ##################################
def clase( request, curso, clase ):
	if not request.user.is_authenticated( ):
		raise Http404
	else:
		curso = get_object_or_404(Curso, slug=curso)
		clase = get_object_or_404(Clase, slug = clase)
		perfil = UserProfile.objects.get( user = request.user )
		recursos = Recurso.objects.filter( clase = clase )
		if perfil.tipo == 1: # Tipo de perfil usuario ( Admin )
			template = "usuarios/clase.html"
		elif perfil.tipo == 2: # Tipo de perfil miembro ( Consumidor )
			template = "miembros/clase.html"
		return render( request, template, { "recursos" : recursos, "curso":curso, "clase":clase } )
############### CRUD ###################
def nuevaClase( request, curso ):
	if not request.user.is_authenticated( ):
		raise Http404
	else:
		perfil = UserProfile.objects.get( user = request.user )
		if perfil.tipo != 1:
			raise Http404
		else:
			if request.method == "POST":
				formulario = nuevaClaseFormulario( request.POST )
				if formulario.is_valid( ) :
					formulario.save(  )
					
					messages.add_message( request, messages.SUCCESS, "Registro de Clase Exitoso")
					return HttpResponseRedirect( '/cursos/'+curso+'/clases/' )
			else: 
				curso = get_object_or_404(Curso, slug=curso)
				nuevaClaseFormulario.base_fields['capitulo'] = forms.ModelChoiceField(queryset= Capitulo.objects.filter(curso=curso))
				formulario = nuevaClaseFormulario(  )
			return  render( request, "usuarios/nuevaClase.html", { "formulario" : formulario, "curso":curso } )

def editarClase( request, clase ):
	if not request.user.is_authenticated( ):
		raise Http404
	else:
		perfil = UserProfile.objects.get( user = request.user )
		if perfil.tipo != 1:
			raise Http404
		else:
			curso = get_object_or_404( Curso, pk = curso )
			if request.method == 'POST':
				formulario = nuevaClaseFormulario( request.POST, instance = curso )
				if formulario.is_valid( ):
					formulario.save()
					messages.add_message( request, message.SUCCESS, "Se editó correctamente" )
			else: 
				formulario = nuevaClaseFormulario( instance = curso )
			return render( request, 'usuarios/nuevaClase.html', { "formulario" : formulario } )
#########################################################################

##################### Capitulo ##########################################

def capitulos ( request, curso ):
	if not request.user.is_authenticated():
		raise Http404
	else:
		perfil = UserProfile.objects.get( user = request.user )
		if perfil.tipo != 1:
			raise Http404
		else:
			curso = get_object_or_404( Curso, slug = curso )
			capitulos = Capitulo.objects.filter( curso = curso )
			return render( request, "usuarios/capitulos.html", { "curso" : curso, "capitulos" : capitulos } )
######### CRUD #############

def nuevoCapitulo ( request, curso ):
	if not request.user.is_authenticated():
		raise Http404
	else:
		perfil = UserProfile.objects.get( user = request.user )
		if perfil.tipo != 1:
			raise Http404
		else:
			if request.method == "POST": 
				formulario = nuevoCapituloFormulario( request.POST )
				if formulario.is_valid():
					nuevo_capitulo = formulario.save( commit = False )
					nuevo_capitulo.curso = get_object_or_404(Curso, slug=curso)
					nuevo_capitulo.save()

					messages.add_message( request, messages.SUCCESS, "Registro de Capitulo exitoso" )
					return HttpResponseRedirect( '/cursos/'+ curso +'/capitulos/' )
			else:
				formulario = nuevoCapituloFormulario()
				curso = get_object_or_404(Curso,slug=curso)
			return render ( request, "usuarios/nuevoCapitulo.html", { "formulario" : formulario, 'curso':curso } )

def borrarCapitulo (request, curso, capitulo):
	if not request.user.is_authenticated():
		raise Http404
	else:
		perfil = UserProfile.objects.get( user = request.user )
		if perfil.tipo != 1:
			raise Http404
		else:
			messages.add_message( request, messages.SUCCESS, "Se eliminó correctamente el capítulo" )
			(get_object_or_404(Capitulo, pk = capitulo)).delete()
			return HttpResponseRedirect( '/cursos/'+ curso +'/capitulos/' )
##############################################################################################################3

############################## FOROS ############################################################
def foros ( request, curso ):
	if not request.user.is_authenticated():
		raise Http404
	else:
		perfil = UserProfile.objects.get( user = request.user )
		curso = get_object_or_404(Curso, slug = curso)
		foros = Foro.objects.filter(curso = curso)
		if request.user.get_profile().tipo == 1:
			return render ( request, "usuarios/foros.html", { "curso" : curso, "foros" : foros })
		else:
			return render ( request, "miembros/foros.html", { "curso" : curso, "foros" : foros })
#################################################################################################

############################ FORO #############################################3
def foro (request, curso, foro):
	if not request.user.is_authenticated():
		raise Http404
	else:
		curso = get_object_or_404(Curso, slug = curso )
		foro = get_object_or_404(Foro, pk = foro)
		comentarios = Foro_Comentario.objects.filter(foro = foro)
		if request.user.get_profile().tipo == 1:
			return render( request, "usuarios/foro.html", { "curso" : curso, "foro" : foro, "comentarios" : comentarios } )
		else:
			return render( request, "miembros/foro.html", { "curso" : curso, "foro" : foro, "comentarios" : comentarios } )


############# CRUD ####################
def nuevoForo(request, curso):
	if not request.user.is_authenticated():
		raise Http404
	else: 
		perfil = UserProfile.objects.get( user = request.user )
		curso = get_object_or_404(Curso, slug = curso)
		if perfil.tipo != 1 and perfil.user != curso.usuario:
			raise Http404
		else:
			if request.method == "POST":
				formulario = nuevoForoFormulario( request.POST )
				if formulario.is_valid():
					nuevo_foro = formulario.save(commit=False)
					nuevo_foro.curso = curso
					nuevo_foro.save()
					messages.add_message(request, messages.SUCCESS, "Registro de Foro Exitoso")
					return HttpResponseRedirect('/cursos/'+ str(curso.slug) +'/foros/')
			else:
				formulario = nuevoForoFormulario()
			return render(request, "usuarios/nuevoForo.html", { "formulario" : formulario, 'curso':curso })

def borrarForo(request, curso, foro):
	if not request.user.is_authenticated():
		raise Http404
	else: 
		perfil = UserProfile.objects.get( user = request.user )
		curso = get_object_or_404(Curso, slug = curso)
		if perfil.tipo != 1 and perfil.user != curso.usuario:
			raise Http404
		else:
			(get_object_or_404(claseForo, slug = foro)).delete()

def comentarForo(request, curso, foro):
	if not request.user.is_authenticated():
		raise Http404
	else: 
		curso = get_object_or_404(Curso, slug = curso )
		foro = get_object_or_404(Foro, pk = foro)
		perfil = get_object_or_404(UserProfile, user = request.user)
		if request.method == "POST":
			formulario = comentarForoFormulario (request.POST)
			if formulario.is_valid():
				nuevo_comentario = formulario.save(commit=False)
				nuevo_comentario.usuario = perfil.user
				nuevo_comentario.foro = foro
				nuevo_comentario.save()
				messages.add_message(request, messages.SUCCESS, "Registro de comentario exitoso")
				return HttpResponseRedirect('/cursos/'+ str(curso.slug) +'/foros/'+str(foro.id)+'/')
		else:
			formulario = comentarForoFormulario()
		if request.user.get_profile().tipo == 1:
			return render(request, "usuarios/comentarioForo.html", {"curso":curso, "foro":foro, "perfil":perfil, "formulario":formulario})
		else:
			return render(request, "miembros/comentarioForo.html", {"curso":curso, "foro":foro, "perfil":perfil, "formulario":formulario})

#####################################################################################################

############################## Avisos ##############################################################

def avisos(request, curso):
	if not request.user.is_authenticated():
		raise Http404
	else:
		curso = get_object_or_404(Curso, slug = curso)
		perfil = get_object_or_404(UserProfile, user = request.user)
		avisos = Aviso.objects.filter(curso = curso)
		if request.user.get_profile().tipo == 1:
			return render(request, "usuarios/avisos.html", {"curso":curso, "perfil":perfil, "avisos":avisos})
		else:
			return render(request, "miembros/avisos.html", {"curso":curso, "perfil":perfil, "avisos":avisos})

def aviso(request, curso, aviso):
	if not request.user.is_authenticated():
		raise Http404
	else:
		curso = get_object_or_404(Curso, slug=curso)
		perfil = get_object_or_404(UserProfile, user = request.user)
		aviso = get_object_or_404(Aviso, id = aviso)
		if request.user.get_profile().tipo == 1:
			return render(request, "usuarios/aviso.html", {"curso":curso, "perfil":perfil, "aviso":aviso})
		else:
			return render(request, "miembros/aviso.html", {"curso":curso, "perfil":perfil, "aviso":aviso})

def nuevoAviso(request, curso):
	if not request.user.is_authenticated():
		raise Http404
	else:
		curso = get_object_or_404(Curso, slug = curso)
		perfil = get_object_or_404(UserProfile, user = request.user)
		if request.method == "POST":
			formulario = nuevoAvisoFormulario(request.POST)
			if formulario.is_valid():
				nuevo_aviso = formulario.save(commit=False)
				nuevo_aviso.curso = curso
				nuevo_aviso.save()
				messages.add_message(request, messages.SUCCESS, "Registro del Aviso exitoso")
				return HttpResponseRedirect("/cursos/" + curso.slug + "/avisos/")
		else:
			formulario = nuevoAvisoFormulario()
		return render(request, "usuarios/nuevoAviso.html", {"curso": curso, "perfil":perfil, "formulario":formulario})

def borrarAviso(request, curso, aviso):
	if not request.user.is_authenticated():
		raise Http404
	else:
		perfil = UserProfile.objects.get (user = request.user)
		if perfil.tipo != 1:
			raise Http404
		else:
			(get_object_or_404(Aviso, id=aviso)).delete()
			return HttpResponseRedirect("/")

#############################################################################################################################
#############################################################################################################################
# miembros

def miembros(request, curso):
	if not request.user.is_authenticated():
		raise Http404
	else:
		perfil = UserProfile.objects.get( user = request.user )
		cur = get_object_or_404(Curso, slug = curso)
		if request.user.get_profile().tipo == 1:
			return render(request, "usuarios/miembros.html", {"curso":cur, "perfil":perfil, "miembros":cur.miembros.all()})
		else:
			return render(request, "miembros/miembros.html", {"curso":cur, "perfil":perfil, "miembros":cur.miembros.all()})

#### Hay que hacer un debug
def nuevoMiembro(request, curso):
	if not request.user.is_authenticated():
		raise Http404
	else:
		perfil = UserProfile.objects.get( user = request.user )
		cur = get_object_or_404(Curso, slug = curso)
		if perfil.tipo != 1:
			raise Http404
		else: 
			if request.method == "POST":
				formulario_usuario = registrationForm(request.POST)
				formulario_perfil = editarPerfilFormulario(request.POST)
							
				if formulario_usuario.is_valid() and formulario_perfil.is_valid():
					nuevo_miembro = formulario_usuario.save(commit=False)		
					nuevo_miembro.username = formulario_usuario.cleaned_data["email"]
					nuevo_miembro.set_password(formulario_usuario.cleaned_data["password2"])
					nuevo_miembro.save()
					nuevo_perfil = formulario_perfil.save(commit=False)
					nuevo_perfil.tipo = 2
					nuevo_perfil.user = nuevo_miembro	
					nuevo_perfil.save()

					cur.miembros.add(nuevo_miembro)		
					return HttpResponseRedirect("/cursos/" + cur.slug + "/miembros/")			
			else:
				formulario_usuario = registrationForm()
				formulario_perfil = editarPerfilFormulario()
			return render(request, "usuarios/nuevoMiembro.html", {"perfil":perfil, "curso":cur, "formulario1":formulario_usuario, "formulario2":formulario_perfil })

#############################################################################################
# Quizes

def quizes(request, curso):
	if not request.user.is_authenticated() : 
		raise Http404
	else:
		perfil = UserProfile.objects.get( user = request.user )
		cur = get_object_or_404(Curso, slug = curso)
		if request.user.get_profile().tipo == 1:
			quizes = Quiz.objects.filter(curso = cur)
			return render(request, "usuarios/quizes.html", {"perfil":perfil, "curso":cur, "quizes":quizes})	
		else:
			aplicaciones = Quiz.objects.filter(quiz_aplicar__usuario=request.user)
			quizos = Quiz.objects.filter(curso = cur, fecha_limite__gte=datetime.datetime.now())
			quizes = set()
			for q in quizos:
				entregado = 0
				for a in aplicaciones:
					if q == a:
						entregado = 1
				if entregado == 0:
					quizes.add(q) 

			return render(request, "miembros/quizes.html", {"perfil":perfil, "curso":cur, "quizes":quizes, "aplicaciones":aplicaciones})

def nuevoQuiz(request, curso):
	if not request.user.is_authenticated():
		raise Http404
	else:
		perfil = UserProfile.objects.get(user = request.user)
		cur = get_object_or_404(Curso, slug = curso)
		if request.method == "POST":
			formulario = nuevoQuizFormulario(request.POST)
			if formulario.is_valid():
				nuevo_quiz = formulario.save(commit=False)
				nuevo_quiz.curso = cur
				nuevo_quiz.save()
				return HttpResponseRedirect("/cursos/" + cur.slug + "/quizzes/")
		else:
			formulario = nuevoQuizFormulario()
		return render(request, "usuarios/nuevoQuiz.html", {"perfil":perfil, "curso":cur, "formulario":formulario})

def quiz(request, curso, quiz):
	if not request.user.is_authenticated():
		raise Http404
	else:
		entregas = Quiz_Aplicar.objects.filter(quiz=quiz, usuario=request.user)
		cur = get_object_or_404(Curso, slug = curso)
		q = get_object_or_404(Quiz, id = quiz)
		preguntas = Quiz_Pregunta.objects.filter(prueba = q)
		perfil = UserProfile.objects.get(user = request.user)

		if request.user.get_profile().tipo == 1:
			return render(request, "usuarios/quiz.html", {"perfil":perfil, "curso":cur, "quiz":q, "preguntas":preguntas})
		else:
			if entregas.count() > 0:
				messages.add_message(request, messages.ERROR, "No puedes realizar esta prueba, ya la hiciste anteriormente.")
				return redirect('/cursos/'+ curso +'/quizzes/')

			if request.method == 'POST':
				aplicacion = Quiz_Aplicar()
				aplicacion.usuario = request.user
				aplicacion.quiz = q
				aplicacion.fecha_inicio = '2014-12-12 00:00:00'
				aplicacion.fecha_termino = '2014-12-12 00:00:00'
				aplicacion.save()

				for pregunta in preguntas:
					formulario = Quiz_Respuesta()
					formulario.examen = aplicacion
					formulario.respuesta = request.POST['respuesta-'+str(pregunta.id)]
					formulario.pregunta = pregunta
					formulario.feedback = ''
					formulario.save()

				return redirect('/cursos/'+ curso +'/')
			else:

				return render(request, "miembros/quiz.html", {"perfil":perfil, "curso":cur, "quiz":q, "preguntas":preguntas, "entregas":entregas })

def borrarQuiz(request, curso, quiz):
	if not request.user.is_authenticated():
		raise Http404
	else:
		perfil = UserProfile.objects.get (user = request.user)
		if perfil.tipo != 1:
			raise Http404
		else:
			(get_object_or_404(Quiz, id=quiz)).delete()
			return HttpResponseRedirect("/curso/" + curso + "/quizzes/")	

def nuevaPregunta(request, curso, quiz):
	if not request.user.is_authenticated():
		raise Http404
	else:
		cur = get_object_or_404(Curso, slug = curso)
		q = get_object_or_404(Quiz, id = quiz)
		perfil = UserProfile.objects.get(user = request.user)
		if request.method == "POST":
			formulario = nuevaPreguntaFormulario(request.POST)
			if formulario.is_valid():
				nueva_pregunta  = formulario.save(commit = False)
				nueva_pregunta.prueba = q
				nueva_pregunta.save()
				return HttpResponseRedirect("/cursos/" + cur.slug + "/quizzes/" + quiz + "/")
		else:
			formulario = nuevaPreguntaFormulario()
		return render(request, "usuarios/nuevaPregunta.html", {"perfil":perfil, "curso":cur, "quiz":q, "formulario":formulario})

def borrarPregunta(request, curso, quiz, pregunta):
	if not request.user.is_authenticated():
		raise Http404
	else:
		perfil = UserProfile.objects.get (user = request.user)
		if perfil.tipo != 1:
			raise Http404
		else:
			(get_object_or_404(Quiz_Pregunta, id=pregunta)).delete()
			return HttpResponseRedirect("/curso/" + curso + "/quizes/" + quiz + "/")

def preguntas(request, curso, quiz, pregunta):
	if not request.user.is_authenticated():
		raise Http404
	else:
		cur = get_object_or_404(Curso, slug = curso)
		q = get_object_or_404(Quiz, id = quiz)
		p = get_object_or_404(Quiz_Pregunta, id = pregunta)
		respuestas = Quiz_Respuesta.objects.filter(pregunta = p)
		perfil = UserProfile.objects.get(user = request.user)
		return render(request, "usuarios/pregunta.html", {"perfil":perfil, "curso":cur, "quiz":q, "pregunta":p, "respuestas":respuestas})

def nuevaRespuesta(request, curso, quiz, pregunta):
	if not request.user.is_authenticated():
		raise Http404
	else:
		cur = get_object_or_404(Curso, slug = curso)
		q = get_object_or_404(Quiz, id = quiz)
		p = get_object_or_404(Quiz_Pregunta, id = pregunta)
		perfil = UserProfile.objects.get(user = request.user)
		if request.method == "POST":
			formulario = nuevaRespuestaFormulario(request.POST)
			if formulario.is_valid():
				nueva_respuesta = formulario.save(commit=False)
				nueva_respuesta.pregunta = p
				nueva_respuesta.save()
				return HttpResponseRedirect("/cursos/" + cur.slug + "/quizzes/" + quiz + "/preguntas/" + pregunta + "/")
		else:
			formulario = nuevaRespuestaFormulario()
		return render(request, "usuarios/nuevaRespuesta.html", {"perfil":perfil, "curso":cur, "quiz":q, "pregunta":p ,"formulario":formulario})

def borrarRespuesta(request, curso, quiz, pregunta, respuesta):
	if not request.user.is_authenticated():
		raise Http404
	else:
		perfil = UserProfile.objects.get (user = request.user)
		if perfil.tipo != 1:
			raise Http404
		else:
			(get_object_or_404(Quiz_Respuesta, id=respuesta)).delete()
			return HttpResponseRedirect("/curso/" + curso + "/quizes/" + quiz + "/" + pregunta + "/")

def envivo(request, curso):
	if not request.user.is_authenticated():
		raise Http404	
	
	if request.user.userprofile.tipo == 1:
		cur = get_object_or_404(Curso, slug = curso)
		if request.method == "POST":
			formulario = nuevoCanalCursoFormulario(request.POST, instance=cur)
			if formulario.is_valid():							
				formulario.save()
				return HttpResponseRedirect("/cursos/" + cur.slug + "/")
		else:
			formulario = nuevoCanalCursoFormulario(instance=cur)
		return render(request, "usuarios/nuevoStream.html", {"curso":cur, "formulario":formulario})

	if request.user.userprofile.tipo == 2:
		cur = get_object_or_404(Curso, slug = curso)
		return render(request, "miembros/stream.html", {"curso":cur, "streamvideo":embed_video(cur.canal)})


def add_slideshare(request, curso, clase):
	if not request.user.is_authenticated():
		raise Http404

	c = get_object_or_404(Curso, slug=curso)
	if request.method == "POST":
		formulario = nuevoRecursoFormulario(request.POST)
		if formulario.is_valid():
			f = formulario.save(commit=False)
			c = get_object_or_404(Clase, slug=clase)
			f.url = id_slide(f.url)
			f.clase = c
			f.tipo = 1
			f.save()
			messages.add_message(request, messages.SUCCESS, "La presentación de slideshare se agregó correctamente")
			return HttpResponseRedirect("/cursos/" + curso + "/"+clase+"/")
	else:
		formulario = nuevoRecursoFormulario()
	return render(request, 'usuarios/nuevoRecurso.html', {'formulario':formulario, 'curso': c })

def add_dropbox(request, curso, clase):
	if not request.user.is_authenticated():
		raise Http404

	c = get_object_or_404(Curso, slug=curso)
	if request.method == "POST":
		formulario = nuevoRecursoFormulario(request.POST)
		if formulario.is_valid():
			f = formulario.save(commit=False)
			c = get_object_or_404(Clase, slug=clase)			
			f.clase = c
			f.tipo = 2
			f.save()
			messages.add_message(request, messages.SUCCESS, "El archivo de dropbox se agregó correctamente")
			return HttpResponseRedirect("/cursos/" + curso + "/"+clase+"/")
	else:
		formulario = nuevoRecursoFormulario()
	return render(request, 'usuarios/nuevoRecurso.html', {'formulario':formulario, 'curso':c})

def add_youtube(request, curso, clase):
	if not request.user.is_authenticated():
		raise Http404

	c = get_object_or_404(Curso, slug=curso)
	if request.method == "POST":
		formulario = nuevoRecursoFormulario(request.POST)
		if formulario.is_valid():
			f = formulario.save(commit=False)
			c = get_object_or_404(Clase, slug=clase)
			f.url = embed_video(f.url)
			f.clase = c
			f.tipo = 3
			f.save()
			messages.add_message(request, messages.SUCCESS, "El video de YouTube se agregó correctamente")
			return HttpResponseRedirect("/cursos/" + curso + "/"+clase+"/")
	else:
		formulario = nuevoRecursoFormulario()
	return render(request, 'usuarios/nuevoRecurso.html', {'formulario':formulario, 'curso': c})

def add_weblink(request, curso, clase):
	if not request.user.is_authenticated():
		raise Http404

	c = get_object_or_404(Curso, slug=curso)
	if request.method == "POST":
		formulario = nuevoRecursoFormulario(request.POST)
		if formulario.is_valid():
			f = formulario.save(commit=False)
			c = get_object_or_404(Clase, slug=clase)
			f.clase = c
			f.tipo = 4
			f.save()
			messages.add_message(request, messages.SUCCESS, "El enlace web se registró correctamente")
			return HttpResponseRedirect("/cursos/" + curso + "/"+clase+"/")
	else:
		formulario = nuevoRecursoFormulario()
	return render(request, 'usuarios/nuevoRecurso.html', {'formulario':formulario, 'curso': c })

def tareas(request, curso):
	if not request.user.is_authenticated():
		raise Http404
	c = get_object_or_404(Curso, slug=curso)
	if request.user.get_profile().tipo == 1:
		t = Tarea.objects.filter(curso=c)
		return render(request, 'usuarios/tareas.html', { 'tareas':t, 'curso':c })
	else:
		t = Tarea.objects.filter(curso=c, fecha_limite__gte=datetime.datetime.now())
		return render(request, 'miembros/tareas.html', { 'tareas':t, 'curso':c })	

def nuevoTarea(request, curso):
	if not request.user.is_authenticated():
		raise Http404

	c = get_object_or_404(Curso, slug=curso)
	if request.method == "POST":
		formulario = nuevoTareaFormulario(request.POST)
		if formulario.is_valid():
			f = formulario.save(commit=False)
			f.curso = c
			f.save()
			messages.add_message(request, messages.SUCCESS, "Se registró la tarea correctamente")
			return HttpResponseRedirect("/cursos/" + curso + "/tareas/")
	else:
		formulario = nuevoTareaFormulario()
	return render(request, 'usuarios/nuevoTarea.html', {'formulario':formulario, 'curso':c  })

#Lectura y formulario de entrega para miembros
def tarea(request, curso, tarea):
	if not request.user.is_authenticated():
		raise Http404

	c = get_object_or_404(Curso, slug=curso)
	t = get_object_or_404(Tarea, id=tarea)

	entregas = Entrega_Tarea.objects.filter(tarea=tarea,alumno=request.user)

	if request.method == "POST":
		formulario = nuevoEntregaTareaFormulario(request.POST)
		if formulario.is_valid():
			f = formulario.save(commit=False)
			if entregas.count() > 0:
				entrega = get_object_or_404(Entrega_Tarea, id=entregas[0].pk)
				entrega.comentarios = f.comentarios
				entrega.link_dp = f.link_dp
				entrega.save()
			else:	
				f.tarea = t
				f.alumno = request.user
				f.save()
			return HttpResponseRedirect("/cursos/" + curso + "/tareas/")
	else:
		formulario = nuevoEntregaTareaFormulario()
	return render(request, 'miembros/nuevoTarea.html', {'formulario':formulario, 'curso':c, 'tarea':t, 'entregas':entregas })

def gradecenter(request, curso):
	if not request.user.is_authenticated():
		raise Http404
	c = get_object_or_404(Curso, slug=curso)
	tareas = Tarea.objects.filter(curso=c)
	quizzes = Quiz.objects.filter(curso=c)

	return render(request, 'usuarios/gradecenter.html', { 'tareas':tareas, 'quizzes':quizzes, 'curso':c })


def gradequiz(request, curso, quiz):
	if not request.user.is_authenticated():
		raise Http404

	aplicaciones = Quiz_Aplicar.objects.filter(quiz=quiz)
	c = get_object_or_404(Curso, slug=curso)
	return render(request, 'usuarios/gradequiz.html', { 'aplicaciones':aplicaciones, 'curso':c, 'quiz':quiz })

def gradetarea(request, curso, tarea):
	if not request.user.is_authenticated():
		raise Http404

	entregas = Entrega_Tarea.objects.filter(tarea=tarea)
	c = get_object_or_404(Curso, slug=curso)
	return render(request, 'usuarios/gradetarea.html', { 'entregas':entregas, 'curso':c,  'tarea':tarea })

def gradequiz_aplicacion(request, curso, quiz, aplicacion):
	if not request.user.is_authenticated():
		raise Http404
	else:
		if request.method == "POST":
			for elemento in request.POST:
				if not elemento == 'csrfmiddlewaretoken':					
					respuesta = get_object_or_404(Quiz_Respuesta, id=int(str(elemento).split('-')[1]))
					respuesta.feedback = str(request.POST[elemento])
					respuesta.save()

			respuestas = Quiz_Respuesta.objects.filter(examen=aplicacion)	
			c = get_object_or_404(Curso, slug=curso)
		else:
			respuestas = Quiz_Respuesta.objects.filter(examen=aplicacion)	
			c = get_object_or_404(Curso, slug=curso)
		return render(request, 'usuarios/gradeaplicacion.html', { 'respuestas':respuestas, 'curso':c })

def gradetarea_entrega(request, curso, tarea, entrega):
	if not request.user.is_authenticated():
		raise Http404
	else:
		c = get_object_or_404(Curso, slug=curso)
		entrega = get_object_or_404(Entrega_Tarea, id=tarea)
		if request.method == "POST":
			feedback = request.POST['feedback']			
			entrega.feedback = feedback
			entrega.save()
		return render(request, 'usuarios/gradeentrega.html', { 'entrega':entrega, 'curso':c })


def del_recurso(request, curso, clase, recurso):
	if not request.user.is_authenticated() or not request.user.get_profile().tipo == 1:
		raise Http404

	r = get_object_or_404(Recurso, id=recurso)
	r.delete()
	messages.add_message(request, messages.SUCCESS, "Se eliminó el recurso correctamente")
	return redirect('/cursos/'+ curso +'/'+ clase +'/')

############################ FUNCIONES DE UTILIDAD ###################################3

def id_slide(url):
	sock = urllib.urlopen('http://www.slideshare.net/api/oembed/2?url='+url+'&format=json')
	slideId = json.loads(sock.read())['slideshow_id']
	sock.close()
	return slideId

def embed_video(url):
	sock = urllib.urlopen('http://www.youtube.com/oembed?url='+url+'&format=json')
	video = json.loads(sock.read())['html']
	sock.close()
	return video
