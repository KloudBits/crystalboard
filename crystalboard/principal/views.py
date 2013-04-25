#encoding:utf-8
from django.shortcuts import render_to_response
from principal.models import UserProfile, Lista, Comentario_Tarea, Curso, Aviso, Comentario_Aviso, Tarea, Entrega_Tarea
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from principal.forms import AvisoForm, ComentarioavisoForm, ListaForm
from django.db.models import Avg, Count
from django.template.defaultfilters import slugify
from django.core import serializers
from django.contrib import messages


def nueva_lista(request, cur):
	if not request.user.is_authenticated():
		return redirect('/')

	if request.method == 'POST':
		crso = Curso.objects.get(pk=cur)
		formulario = ListaForm(request.POST)
		if formulario.is_valid():
			nuevalista = formulario.save(commit=False)
			nuevalista.curso = cur
			nuevalista.save()

			messages.add_message(request, messages.SUCCESS, 'Registro de aviso exitoso')
			return HttpResponseRedirect('/' + cur + '/')
	else:
		formulario = ListaForm()
	return render_to_response('lista.html', {'formulario':formulario}, context_instance=RequestContext(request))






def nuevo_aviso(request, cur):
	if not request.user.is_authenticated():
		return redirect('/')

	if request.method == 'POST':
		crso = Curso.objects.get(pk=cur)
		formulario = AvisoForm(request.POST)
		if formulario.is_valid():
			nuevoaviso = formulario.save(commit=False)
			nuevoaviso.curso = crso
			nuevoaviso.save()

			messages.add_message(request, messages.SUCCESS, 'Registro de aviso exitoso.')
			return HttpResponseRedirect('/'+cur+'/')
	else:
		formulario = AvisoForm()
	return render_to_response('aviso.html', {'formulario':formulario}, context_instance=RequestContext(request))



def cursodash(request, cur):
	avisos = Aviso.objects.filter(curso=cur)
	return render_to_response('cursodash.html', {'avisos':avisos, 'curso':cur }, context_instance=RequestContext(request))



def dashboard(request):
	profile = UserProfile.objects.get(user=request.user)
	if profile.tipo == 1 or profile.tipo == 2:
		cursos = Curso.objects.filter(docente=request.user)
	else:
		cursos = Curso.objects.filter(alumnos=request.user)
	return render_to_response('dashboard.html', {'cursos':cursos}, context_instance=RequestContext(request))



def ingreso_usuario(request):
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['usuario']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				login(request, acceso)
				return HttpResponseRedirect('/dashboard/')
			else:
				messages.add_message(request, messages.ERROR, 'El usuario o contraseña son incorrectos')
				return HttpResponseRedirect('/login/')
	else:
		formulario = AuthenticationForm()
	return render_to_response('login.html', {'formulario': formulario}, context_instance=RequestContext(request))
