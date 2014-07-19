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
from Main.models import UserProfile, Curso, Tarea, Clase, Recurso
from Main.forms import nuevoCurso, nuevaClaseFormulario

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
		if perfil.tipo == 1: # Tipo de perfil Usuario ( Admin ) 			
			template = "usuarios/perfil.html"
		elif perfil.tipo == 2: # Tipo de perfil miembro ( Consumidor )			
			template = "miembros/perfil.html"
		return render( request, template, { 'perfil' : perfil } )

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
			cursos = Curso.objects.filter(  ) ######## FALTA
			template = "miembros/cursos.html"
		return render( request, template, {  } )


#########################################################################

###########################    Curso    #################################
def curso( request, curso ):
	if not request.user.is_authenticated( ):
		raise Http404
	else:
		clases = Clase.objects.filter( Curso, pk = curso )
		perfil = UserProfile.objects.get( user = request.user )
		if perfil.tipo == 1: # Tipo de perfil de usuario ( Admin )
			template = "usuarios/curso.html"
		elif perfil.tipo == 2: # Tipo de perfil miembro ( Consumidor )
			template = "miembros/curso.html"
		return render( request, template, { "clases" : clases } )

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
				formulario = nuevoCurso( request.POST, request.FILES )
				if formulario.is_valid( ) and formulario.is_multipart( ):
					nuevo_curso = formulario.save( commit = False )
					nuevo_curso.save( )
					messages.add_message( request, messages.SUCCESS, 'Registro de curso exitoso' )
					return HttpResponseRedirect( '/' )
			else:
				formulario = nuevoCurso( )
	return render( request, 'usuarios/nuevoCurso.html', { "formulario" : formulario } )

def editarCurso( request ):
	return render( request, '', {  } )	
#########################################################################

###############################  Clase ##################################
def clase( request, curso, clase ):
	if not request.user.is_authenticated( ):
		raise Http404
	else:
		clase = get_object_or_404(Clase, pk = clase)
		perfi l = UserProfile.objects.get( user = request.user )
		tareas = Tarea.objects.filter( clase = clase )
		recursos = Recurso.objects.filter( clase = clase )
		if perfil.tipo == 1: # Tipo de perfil usuario ( Admin )
			template = "usuarios/clase.html"
		elif perfil.tipo == 2: # Tipo de perfil miembro ( Consumidor )
			template = "miembros/clase.html"
		return render( request, template, { "tareas" : tareas, "recursos" : recursos } )

########## CRUD ############
def nuevaClase( request ):
	if not request.user.is_authenticated( ):
		raise Http404
	else:
		perfil = UserProfile.objects.get( user = request.user )
		if perfil.tipo != 1:
			raise Http404
		else:
			if request.method == POST:
				formulario = nuevaClaseFormulario( request.POST )
				if formulario.is_valid( ) :
					nueva_clase = formulario.save( commit = False )
					nueva_clase.save( )
					messages.add_message( request, messages.SUCCESS, "Registro de Clase Exitoso")
					return HttpResponseRedirect( '/' )
			else: 
				formulario = nuevaClase( request.POST )
			return  render( request, "usuarios/nuevaClase.html", { "formulario" : formulario } )
#########################################################################



