#encoding:utf-8
from django.shortcuts import render_to_response, render, redirect,get_object_or_404
from principal.models import Instituto, Respuesta, Comentario, Foro, Clase, Infocurso, Asistencia, UserProfile, Lista, Comentario_Tarea, Curso, Aviso, Comentario_Aviso, Tarea, Entrega_Tarea
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from principal.forms import NuevoCursoFormulario, ClaseForm, ComentarioForm, RespuestaForm, ForoForm, ClaseEditarFormulario, InfocursoForm, EntregaForm, TareaForm, AvisoForm, ComentarioavisoForm#, TipoListaForm
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
@login_required(login_url='/login/') ### Se indica que tiene que iniciar sesion
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

def nuevo_lista(request, cur, clse):
    clase = get_object_or_404(Clase, pk=clse)
    try:
        if clase.lista:
            return redirect('/'+cur+'/clases/'+clse+'/lista/')
    except:
        if request.method == 'POST':
            fecha = request.POST['fecha']
            lista = Lista(clase=clase, fecha=fecha)
            lista.save()

            curso = get_object_or_404(Curso, pk=cur)
            alumnos = curso.alumnos.all()
            for a in alumnos:
                asistencia = Asistencia(lista=lista, usuario=a)
                asistencia.save()

            return redirect('/'+cur+'/clases/'+clse+'/lista/')
    return render(request, 'nueva-asistencia.html')

def lista(request, cur, clse):
    clase = get_object_or_404(Clase, pk=clse)
    if request.method == 'POST':
        lista = request.POST.getlist('inalumnos')
        alumnos = Asistencia.objects.filter(lista=clase.lista)
        for a in alumnos:
            encontrado = False
            for l in lista:
                u = get_object_or_404(User, pk=l)
                if a.usuario == u:
                    a.asis = True
                    a.save()
                    encontrado = True
            if not encontrado:
                a.asis = False
                a.save()

        return redirect('/'+cur+'/clases/'+clse+'/lista/')
    else:
        try:
            if clase.lista:
                asistencia = Asistencia.objects.filter(lista=clase.lista)
                return render(request,'asistencia.html',{'alumnos':asistencia, 'clase':clase})
        except:
            return redirect('/'+cur+'/clases/'+clse+'/lista/nuevo/')


# def lista(request, cur, clase):
#     if not request.user.is_authenticated():
#         return HttpResponseRedirect('/')

#     clase = get_object_or_404(Clase, pk=clase)
#     #if request.user.get_profile().tipo == 3:
#     profile = UserProfile.objects.get(user=request.user)
#     if profile.tipo == 3: ## Lo cambie porque me mandaba un error
#         lista = get_object_or_404(Lista, clase=clase)
#         asistencia = Asistencia.objects.filter(usuario=request.user)
#         return render(request, 'asistencia.html', {'asistencia': asistencia, 'lista': lista})

#     alumnos = clase.alumnos.all()

#     if request.method == 'POST':
#         l = Lista(clase=clase, fecha=datetime.today())
#         l.save()
#         encontrado = False #Una bandera para registrar en caso de que no lo lleve el getlist
#         lista = request.POST.getlist('inalumnos')
#         for alumno in alumnos:
#             for ia in lista:
#                 u = get_object_or_404(User, pk=ia)
#                 if alumno == u:
#                     reg = Asistencia(lista=l, usuario=alumno, asis=True)
#                     encontrado = True
#             if encontrado == False:
#                 reg = Asistencia(lista=l, usuario=alumno, asis=False)
#             reg.save()
#         return HttpResponseRedirect('/' + cur + '/')
#     else:
#         asistencia = Asistencia.objects.filter(lista__clase=clase)
#         lista = get_object_or_404(Lista, clase=clase)

#     return render(request, 'asistencia.html', {'alumnos': alumnos, 'asistencia': asistencia, 'lista': lista})


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

@login_required(login_url='/login/') ### Se indica que tiene que iniciar sesion
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
##################################
# Funcion para Crear Nuevo Curso #
##################################
def nuevo_curso(request):
    if not request.user.is_authenticated():
        raise Http404
    profile = UserProfile.objects.get(user=request.user)
    if profile.tipo != 2:
        raise Http404
    else:
        instituto = profile.instituto
        if request.method == 'POST':
            formulario = NuevoCursoFormulario(request.POST, request.FILES)
            if formulario.is_valid() and formulario.is_multipart():
                nuevo_curso = formulario.save(commit=False)
                nuevo_curso.instituto = profile.instituto
                nuevo_curso.save()
                messages.add_message(request, messages.SUCCESS, 'Registro de curso exitoso')
                return HttpResponseRedirect('/dashboard/')
        else:
            formulario = NuevoCursoFormulario()
    return render(request, "nuevo_curso.html", {'formulario' : formulario})

################################################

####################################################


#####################################################

@login_required(login_url='/login/') ### Se indica que tiene que iniciar sesion
def dashboard(request):
    if not request.user.is_authenticated():
        raise Http404

    profile = UserProfile.objects.get(user=request.user)

    if profile.tipo == 2: # Verificar si es director
        cursos = Curso.objects.filter(instituto=profile.instituto)
        return render(request, 'dashboard_director.html', {'cursos':cursos}) # Mostrar plantilla del director
    ################################################
    elif profile.tipo == 1:
        cursos = Curso.objects.filter(docente=request.user)
    else:
        cursos = Curso.objects.filter(alumnos=request.user)
    return render_to_response('dashboard.html', {'cursos': cursos}, context_instance=RequestContext(request))


def egreso_usuario(request):  ### View para cerrar sesion ###
    logout(request)
    return HttpResponseRedirect('/login/')

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
        if not request.user.is_authenticated(): ### Checa si el usuario ya inicio sesion ###
            formulario = AuthenticationForm()
        else:
            return HttpResponseRedirect('/dashboard/')
    return render_to_response('login.html', {'formulario': formulario}, context_instance=RequestContext(request))

def foro(request, cur):
    curso = get_object_or_404(Curso, pk=cur)
    foros = Foro.objects.filter(curso=cur)
    return render(request, 'foro.html', {'foros':foros, 'curso':curso})

def nuevo_foro(request, cur):
    curso = get_object_or_404(Curso, pk=cur)
    if request.method=='POST':
        formulario = ForoForm(request.POST)
        if formulario.is_valid():
            f = formulario.save(commit=False)
            f.curso = curso
            f.save()

            messages.add_message(request, messages.SUCCESS, 'Registro de foro de discusión exitoso.')
            return redirect('/' + cur + '/foro/')
    else:
        formulario = ForoForm()
    return render(request, 'nuevo_comentario.html', {'formulario':formulario})

def ver_foro(request, cur, forr):
    foro = get_object_or_404(Foro, pk=forr)
    return render(request, 'un-foro.html', {'foro':foro})


def nuevo_respuesta(request, cur, forr):
    foro = get_object_or_404(Foro, pk=forr)
    if request.method=='POST':
        formulario = RespuestaForm(request.POST)
        if formulario.is_valid():
            f = formulario.save(commit=False)
            f.foro = foro
            f.usuario = request.user
            f.save()

            messages.add_message(request, messages.SUCCESS, 'Registro de respuesta en discusión exitoso.')
            return redirect('/' + cur + '/foro/'+forr+'/respuesta/')
    else:
        formulario = RespuestaForm()
    return render(request, 'nuevo_comentario.html', {'formulario':formulario})

def ver_comentarios(request, cur, forr, res):
    respuesta = get_object_or_404(Respuesta, pk=res)
    if request.method=='POST':
        formulario = ComentarioForm(request.POST)
        if formulario.is_valid():
            f = formulario.save(commit=False)
            f.respuesta = respuesta
            f.usuario = request.user
            f.save()

            messages.add_message(request, messages.SUCCESS, 'Registro de comentario respuesta exitoso.')
            return redirect('/' + cur + '/foro/'+forr+'/respuesta/'+res+'/comentarios/')
    else:
        formulario = ComentarioForm()
    return render(request, 'nuevo_com_foro.html', {'respuesta':respuesta, 'formulario':formulario})


def panel_asistencia(request, cur):
    listas = Lista.objects.filter(clase__curso=cur)
    return render(request, 'panel-control/asistencia.html', {'listas':listas})



def nuevo_envivo(request, cur, clse):
    curso = get_object_or_404(Curso, pk=cur)
    clase = get_object_or_404(Clase, pk=clse)
    embed = request.POST['envivo']
    clase.stream = embed
    clase.save()
    return redirect('/'+cur+'/clases/'+clse+'/')

def nuevo_presentacion(request, cur, clse):
    curso = get_object_or_404(Curso, pk=cur)
    clase = get_object_or_404(Clase, pk=clse)
    embed = request.POST['slideshare']
    clase.slideshare = embed
    clase.save()
    return redirect('/'+cur+'/clases/'+clse+'/')

def nuevo_recursos(request, cur, clse):
    curso = get_object_or_404(Curso, pk=cur)
    clase = get_object_or_404(Clase, pk=clse)
    embed = request.POST['texto']
    clase.recursos = embed
    clase.save()
    return redirect('/'+cur+'/clases/'+clse+'/')

def nuevo_codigo(request, cur, clse):
    curso = get_object_or_404(Curso, pk=cur)
    clase = get_object_or_404(Clase, pk=clse)
    embed = request.POST['codigo']
    clase.codigo = embed
    clase.save()
    return redirect('/'+cur+'/clases/'+clse+'/')




def clases(request, cur):
    curso = get_object_or_404(Curso, pk=cur)
    clases = Clase.objects.filter(curso=curso)
    return render(request, 'clases.html', {'clases':clases, 'curso':curso})

def nuevo_clase(request, cur):
    curso = get_object_or_404(Curso, pk=cur)
    if request.method=='POST':
        formulario = ClaseForm(request.POST)
        if formulario.is_valid():
            f = formulario.save(commit=False)
            f.curso = curso
            f.save()

            messages.add_message(request, messages.SUCCESS, 'Registro de clase exitoso.')
            return redirect('/' + cur +'/')
    else:
        formulario = ClaseForm()
    return render(request, 'nuevo_comentario.html', {'formulario':formulario})

