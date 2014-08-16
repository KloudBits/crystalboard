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
from Main.models import UserProfile, Curso, Tarea, Clase, Recurso, Capitulo, Foro, Foro_Comentario, Aviso
from Main.forms import nuevoCursoFormulario, nuevaClaseFormulario, nuevoCapituloFormulario, nuevoForoFormulario, nuevoAvisoFormulario, registrationForm, editarPerfilFormulario

########################## LOGEO #######################################
def ingreso_usuario( request ):
	if request.method == 'POST':
		formulario = AuthenticationForm( request.POST )
		if formulario.is_valid:
			usuario = request.POST [ 'usuario' ]
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
		raise Http404
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
		clases = Clase.objects.filter(capitulo__curso__slug = curso )
		perfil = UserProfile.objects.get( user = request.user )
		if perfil.tipo == 1: # Tipo de perfil de usuario ( Admin )
			template = "usuarios/clases.html"
		elif perfil.tipo == 2: # Tipo de perfil miembro ( Consumidor )
			template = "miembros/clases.html"
		return render( request, template, { "clases" : clases } )

###############################  Clase ##################################
def clase( request, curso, clase ):
	if not request.user.is_authenticated( ):
		raise Http404
	else:
		clase = get_object_or_404(Clase, slug = clase)
		perfil = UserProfile.objects.get( user = request.user )
		tareas = Tarea.objects.filter( clase = clase )
		recursos = Recurso.objects.filter( clase = clase )
		if perfil.tipo == 1: # Tipo de perfil usuario ( Admin )
			template = "usuarios/clase.html"
		elif perfil.tipo == 2: # Tipo de perfil miembro ( Consumidor )
			template = "miembros/clase.html"
		return render( request, template, { "tareas" : tareas, "recursos" : recursos } )
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
					nueva_clase = formulario.save( commit = False )
					nueva_clase.save( )
					messages.add_message( request, messages.SUCCESS, "Registro de Clase Exitoso")
					return HttpResponseRedirect( '/' )
			else: 
				formulario = nuevaClaseFormulario( request.POST )
			return  render( request, "usuarios/nuevaClase.html", { "formulario" : formulario } )

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
					return HttpResponseRedirect( '/' )
			else:
				formulario = nuevoCapituloFormulario()
			return render ( request, "usuarios/nuevoCapitulo.html", { "formulario" : formulario } )

def borrarCapitulo (request, curso, capitulo):
	if not request.user.is_authenticated():
		raise Http404
	else:
		perfil = UserProfile.objects.get( user = request.user )
		if perfil.tipo != 1:
			raise Http404
		else:
			(get_object_or_404(Capitulo, pk = capitulo)).delete()
			return HttpResponseRedirect( "/" )
##############################################################################################################3

############################## FOROS ############################################################
def foros ( request, curso ):
	if not request.user.is_authenticated():
		raise Http404
	else:
		perfil = UserProfile.objects.get( user = request.user )
		curso = get_object_or_404(Curso, slug = curso)
		foros = Foro.objects.filter(curso = curso)
		return render ( request, "usuarios/foros.html", { "curso" : curso, "foros" : foros })
#################################################################################################

############################ FORO #############################################3
def foro (request, curso, foro):
	if not request.usuer.is_authenticated():
		raise Http404
	else:
		curso = get_object_or_404(Curso, slug = curso )
		foro = get_object_or_404(Foro, pk = foro)
		comentarios = Foro_Comentario.objects.filter(foro = foro)
		return render( request, "usuarios/foro.html", { "curso" : curso, "foro" : foro, "comentarios" : comentarios } )

############# CRUD ####################
def nuevoForo(request, curso):
	if not request.usuer.is_authenticated():
		raise Http404
	else: 
		perfil = UserProfile.objects.get( user = request.user )
		curso = get_object_or_404(Curso, pk = curso)
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
					return HttpResponseRedirect('/')
			else:
				formulario = nuevoForoFormulario()
			return render(request, "usuarios/nuevoForo.html", { "formulario" : formulario })

def borrarForo(request, curso, foro):
	if not request.usuer.is_authenticated():
		raise Http404
	else: 
		perfil = UserProfile.objects.get( user = request.user )
		curso = get_object_or_404(Curso, pk = curso)
		if perfil.tipo != 1 and perfil.user != curso.usuario:
			raise Http404
		else:
			(get_object_or_404(Foro, pk = foro)).delete()

def comentarForo(request, curso, foro):
	if not request.usuer.is_authenticated():
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
				nuevo_comentario.save()
				messages.add_message(request, messages.SUCCESS, "Registro de comentario exitoso")
				return HttpResponseRedirect("/")
		else:
			formulario = comentarioForoFormulario()
		return render(request, "usuarios/comentarioForo.html", {"curso":curso, "foro":foro, "perfil":perfil, "formulario":formulario})

#####################################################################################################

############################## Avisos ##############################################################

def avisos(request, curso):
	if not request.user.is_authenticated():
		raise Http404
	else:
		curso = get_object_or_404(Curso, slug = curso)
		perfil = get_object_or_404(UserProfile, user = request.user)
		avisos = Aviso.objects.filter(curso = curso)
		return render(request, "usuarios/avisos.html", {"curso":curso, "perfil":perfil, "avisos":avisos})

def aviso(request, curso, aviso):
	if not request.user.is_authenticated():
		raise Http404
	else:
		curso = get_object_or_404(Curso, slug=curso)
		perfil = get_object_or_404(UserProfile, user = request.user)
		aviso = get_object_or_404(Aviso, id = aviso)
		return render(request, "usuarios/aviso.html", {"curso":curso, "perfil":perfil, "aviso":aviso})

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
				return HttpResponseRedirect("cursos/" + curso.slug + "/avisos/")
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
		return render(request, "usuarios/miembros.html", {"curso":cur, "perfil":perfil, "miembros":cur.miembros})


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
				formulario_perfil.usuario = formulario_usuario.user				
				if formulario_usuario.is_valid() and formulario_perfil.is_valid():
					nuevo_miembro = formulario_usuario.save()					
					cur.miembros.add(nuevo_miembro)		
					return redirect("/cursos/" + cur.slug + "/")			
			else:
				formulario_usuario = registrationForm()
				formulario_perfil = editarPerfilFormulario()
			return render(request, "usuarios/nuevoMiembro.html", {"perfil":perfil, "curso":cur, "formulario1":formulario_usuario, "formulario2":formulario_perfil })

#############################################################################################









