#encoding:utf-8
from django.shortcuts import render_to_response, render, redirect,get_object_or_404
from principal.models import Clase, Infocurso, Asistencia, UserProfile, Lista, Comentario_Tarea, Curso, Aviso, Comentario_Aviso, Tarea, Entrega_Tarea
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from principal.forms import ClaseEditarFormulario, InfocursoForm, EntregaForm, TareaForm, AvisoForm, ComentarioavisoForm#, TipoListaForm
from django.db.models import Avg, Count
from django.template.defaultfilters import slugify
from django.core import serializers
from django.contrib import messages
from datetime import datetime
from django.http import Http404
#from dropbox import client, rest, session
from django.core.mail import send_mail


# Get your app key and secret from the Dropbox developer website
#APP_KEY = 'bzs0qqplfq66m0i'
#APP_SECRET = '6udw3310r6n2yx9'

# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
#ACCESS_TYPE = 'app_folder'
#sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)



# def prueba(request, cur):
#     curso = Curso.objects.get(pk=cur)
#     if not request.user.is_authenticated():
#         return HttpResponseRedirect('/')
#     if request.method == 'POST':
#         lista_inasistencia = request.POST.getlist('inalumnos')
#         for ia in lista_inasistencia:
#             u = User.objects.get(pk=ia)
#             reg = Lista(curso=curso,usuario=u,fecha=datetime.today())
#             reg.save()
#             return HttpResponseRedirect('/')
#     else:
#         s = request.session['fecha']
#         curso = Curso.objects.get(pk=cur) # se obtiene una referencia del curso
#         alumnos = curso.alumnos.all()  # Se obtienen todos los alumnos inscritos

#     return render(request, 'prueba.html', {'mensaje': s, 'alumnos': alumnos})
def perfil(request):
    return render(request, 'perfil.html')

#def conectar_dropbox(request):
    #request_token = sess.obtain_request_token()
    #url = sess.build_authorize_url(request_token, oauth_callback='http://google.com')
    #return redirect(url)
    
def docente(request, cur):
    if not request.user.is_authenticated():
        raise Http404

    curso = get_object_or_404(Curso, pk=cur)
    return render(request, 'docente.html', {'curso' : curso})

def clase(request, cur, cls):
    if not request.user.is_authenticated():
        raise Http404

    curso = get_object_or_404(Curso, pk=cur)
    clase = get_object_or_404(Clase, pk=cls)
    return render(request, 'clase.html', { 'curso' : curso, 'clase' : clase })

def editar_clase(request, cur, cls):
    if not request.user.is_authenticated():
        raise Http404
    if not request.user.get_profile().tipo == 1 and not request.user.get_profile().tipo == 2:
        raise Http404

    curso = get_object_or_404(Curso, pk=cur)
    clase = get_object_or_404(Clase, pk=cls)

    if request.method == 'POST':
        formulario = ClaseEditarFormulario(request.POST, instance=clase)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, messages.SUCCESS, 'Se editó esta clase')
            return HttpResponseRedirect('/' + cur + '/clases/'+cls+'/')
    else:
        formulario = ClaseEditarFormulario(instance=clase)
    return render(request, 'editar-clase.html', { 'formulario': formulario, 'curso' : curso, 'clase' : clase })    

def directorio(request, cur):
    if not request.user.is_authenticated():
        raise Http404

    curso = get_object_or_404(Curso, pk=cur)
    return render(request, 'directorio.html', {'curso' : curso}) 

def informacion(request, cur):
    if not request.user.is_authenticated():
        raise Http404

    curso = get_object_or_404(Curso, pk=cur)
    informacion = Infocurso.objects.filter(curso=curso)

    if request.method == 'POST':
        formulario = InfocursoForm(request.POST)
        if formulario.is_valid():
            f = formulario.save(commit=False)
            f.curso = curso
            f.save()

            messages.add_message(request, messages.SUCCESS, 'Se registro nueva información')
            return HttpResponseRedirect('/' + cur + '/')
    else:
        formulario = InfocursoForm()

    return render(request, 'informacion.html', { 'informacion' : informacion, 'formulario' : formulario })

def tarea(request, cur, tar):
    tarea = get_object_or_404(Tarea, pk=tar)
    profile = UserProfile.objects.get(user=request.user)
    if profile.tipo == 1 or profile.tipo == 2: ## Agrege estas lineas porque me marcaba un error
        entregas = Entrega_Tarea.objects.filter(tarea=tarea)
        return render(request, 'tarea.html', {'tarea': tarea, 'entregas': entregas})

    if request.method == 'POST':
        formulario = EntregaForm(request.POST)
        if formulario.is_valid():
            f = formulario.save(commit=False)
            f.tarea = tarea
            f.alumno = request.user
            f.save()

            messages.add_message(request, messages.SUCCESS, 'Entrega de tarea exitoso.')
            return HttpResponseRedirect('/' + cur + '/')
    else:
        formulario = EntregaForm()
    return render(request, 'tarea.html', {'tarea': tarea, 'formulario': formulario})


def tareas(request, cur):
    if not request.user.is_authenticated():
        raise HttpResponseRedirect('/')

    curso = get_object_or_404(Curso, pk=cur)
    tareas = Tarea.objects.filter(curso=curso)
    if request.method == 'POST':
        formulario = TareaForm(request.POST)
        if formulario.is_valid():
            f = formulario.save(commit=False)
            f.curso = curso
            f.fecha_registro = datetime.today()
            f.save()

            #se obtienen todos los Usuarios inscritos al curso
            alumnos = User.objects.filter(curso=curso)
            # Se crea una lista de destinatarios
            para = []
            for alumno in alumnos: # Se itera atravez de la lista
                if UserProfile.objects.get(user=alumno).tipo == 3: # Se verifica que sea un alumno
                    para.append(alumno.email) # Se agrega el correo del alumno a la lista de destinatarios
            ## Se manda el correo
            send_mail("Nueva Tarea agregada", "Se agrego una nueva tarea al curso " + curso.nombre, "webmaster@crystalboard.com",
                      para)

            messages.add_message(request, messages.SUCCESS, 'Registro de tarea exitoso.')
            return HttpResponseRedirect('/' + cur + '/')
    else:
        formulario = TareaForm()
        #request_token = sess.obtain_request_token()
        #url = sess.build_authorize_url(request_token, oauth_callback='http://google.com')
        #return redirect(url)

    return render(request, 'tareas.html', {'tareas': tareas, 'curso': curso, 'formulario': formulario})


def listas(request, cur):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    curso = get_object_or_404(Curso, pk=cur)
    #if request.user.get_profile().tipo == 3:
    profile = UserProfile.objects.get(user=request.user)
    if profile.tipo == 3: ## Lo cambie porque me mandaba un error
        lista = Lista.objects.filter(curso=curso)
        asistencia = Asistencia.objects.filter(usuario=request.user)
        return render(request, 'asistencia.html', {'asistencia': asistencia, 'lista': lista})

    alumnos = curso.alumnos.all()

    if request.method == 'POST':
        l = Lista(curso=curso, fecha=datetime.today())
        l.save()
        encontrado = False #Una bandera para registrar en caso de que no lo lleve el getlist
        lista = request.POST.getlist('inalumnos')
        for alumno in alumnos:
            for ia in lista:
                u = get_object_or_404(User, pk=ia)
                if alumno == u:
                    reg = Asistencia(lista=l, usuario=alumno, asis=True)
                    encontrado = True
            if encontrado == False:
                reg = Asistencia(lista=l, usuario=alumno, asis=False)
            reg.save()
        return HttpResponseRedirect('/' + cur + '/')
    else:
        asistencia = Asistencia.objects.filter(lista__curso=curso)
        lista = Lista.objects.filter(curso=curso)

    return render(request, 'asistencia.html', {'alumnos': alumnos, 'asistencia': asistencia, 'lista': lista})


def nuevo_aviso(request, cur):
    if not request.user.is_authenticated():
        raise Http404
    if not request.user.get_profile().tipo == 1 and not request.user.get_profile().tipo == 2:
        raise Http404

    if request.method == 'POST':
        crso = get_object_or_404(Curso, pk=cur)
        formulario = AvisoForm(request.POST)
        if formulario.is_valid():
            nuevoaviso = formulario.save(commit=False)
            nuevoaviso.curso = crso
            nuevoaviso.save()

            #se obtienen todos los Usuarios inscritos al curso
            alumnos = User.objects.filter(curso=crso)
            # Se crea una lista de destinatarios
            para = []
            for alumno in alumnos: # Se itera atravez de la lista
                if UserProfile.objects.get(user=alumno).tipo == 3: # Se verifica que sea un alumno
                    para.append(alumno.email) # Se agrega el correo del alumno a la lista de destinatarios
                ## Se manda el correo
            send_mail("Nueva Tarea agregada", "Se agrego un nuevo aviso al curso " + crso.nombre, "webmaster@crystalboard.com",
                      para)

            messages.add_message(request, messages.SUCCESS, 'Registro de aviso exitoso.')
            return HttpResponseRedirect('/' + cur + '/')
    else:
        formulario = AvisoForm()
    return render_to_response('aviso.html', {'formulario': formulario}, context_instance=RequestContext(request))


def cursodash(request, cur):
    if not request.user.is_authenticated():
        raise Http404

    curso = get_object_or_404(Curso, pk=cur)
    avisos = Aviso.objects.filter(curso=cur).annotate(num=Count('comentario_aviso'))
    if request.method == 'POST':
        formulario = AvisoForm(request.POST)
        if formulario.is_valid():
            nuevoaviso = formulario.save(commit=False)
            nuevoaviso.curso = curso
            nuevoaviso.save()

            messages.add_message(request, messages.SUCCESS, 'Registro de aviso exitoso.')
            return HttpResponseRedirect('/' + cur + '/')
    else:
        formulario = AvisoForm()

    return render_to_response('cursodash.html', {'avisos': avisos, 'curso': curso, 'formulario': formulario},
                              context_instance=RequestContext(request))


def comentarios(request, cur, avso):
    if not request.user.is_authenticated():
        raise Http404

    curso = get_object_or_404(Curso, pk=cur)
    aviso = get_object_or_404(Aviso, pk=avso)

    comentarios = Comentario_Aviso.objects.filter(aviso=avso)

    if request.method == 'POST':
        formulario = ComentarioavisoForm(request.POST)
        if formulario.is_valid():
            nuevo_comentario = formulario.save(commit=False)
            nuevo_comentario.aviso = aviso
            nuevo_comentario.usuario = request.user
            nuevo_comentario.save()

            messages.add_message(request, messages.SUCCESS, 'Registro de comentario exitoso')
            return HttpResponseRedirect('/' + cur + '/')
    else:
        formulario = ComentarioavisoForm()
    return render(request, 'lista_comentarios_aviso.html',
                  {'formulario': formulario, 'curso': curso, 'aviso': aviso, 'comentarios': comentarios})


def nuevo_comentario(request, cur, avso):
    if not request.user.is_authenticated():
        raise Http404

    if request.method == 'POST':
        crso = get_object_or_404(Curso, pk=cur)
        aviso = get_object_or_404(Aviso, pk=avso)
        formulario = ComentarioavisoForm(request.POST)
        if formulario.is_valid():
            nuevo_comentario = formulario.save(commit=False)
            nuevo_comentario.aviso = aviso
            nuevo_comentario.usuario = request.user
            nuevo_comentario.save()

            messages.add_message(request, messages.SUCCESS, 'Registro de comentario exitoso')
            return HttpResponseRedirect('/' + cur + '/')
    else:
        formulario = ComentarioavisoForm()
    return render(request, 'nuevo_comentario.html', {'formulario': formulario})


def dashboard(request):
    if not request.user.is_authenticated():
        raise Http404

    profile = UserProfile.objects.get(user=request.user)
    if profile.tipo == 1 or profile.tipo == 2:
        cursos = Curso.objects.filter(docente=request.user)
    else:
        cursos = Curso.objects.filter(alumnos=request.user)
    return render_to_response('dashboard.html', {'cursos': cursos}, context_instance=RequestContext(request))


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
