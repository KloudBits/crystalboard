# encoding: utf-8
from principal.models import Asistencia, Curso, Aviso, Comentario_Aviso, Tarea, Entrega_Tarea, Comentario_Tarea, Lista, UserProfile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'perfiles'

# Definimos un  nuevo User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )


#Definicion de un nuevo curso
class CursoAdmin(admin.ModelAdmin):
	fieldsets = [
		('Nombre del Curso:', {'fields':['nombre']}),
		('Docente que lo imparte:', {'fields':['docente']}),
		('Alumnos asignados al curso:', {'fields':['alumnos']}) 
	]

class AvisoAdmin(admin.ModelAdmin):
	fieldsets = [
		('Aviso al Curso:', {'fields':['curso']}), 
		('Aviso:', {'fields':['texto']})
	]

class Comentario_AvisoAdmin(admin.ModelAdmin):
	fieldsets = [
		('Comentario de:', {'fields':['usuario']}),
		('Aviso comentado:', {'fields':['aviso']}),
		('Comentario:', {'fields':['texto']})
	]

class TareaAdmin(admin.ModelAdmin):
	fieldsets = [
		('Titulo de la Tarea:', {'fields':['titulo']}),
		('Descripcion de la tarea:', {'fields':['descripcion']}),
		(None, {'fields':['fecha_registro', 'fecha_limite']}),
		('Calificacion:', {'fields': ['puntos']}),
		('Tarea del curso:', {'fields': ['curso']})
	]

class Entrega_TareaAdmin(admin.ModelAdmin):
	fieldsets = [
		('Tarea:', {'fields':['tarea']}),
		('Fecha de entrega:', {'fields':['fecha']}),
		('Archivo', {'fields':['archivo']}),
		('Comentarios:', {'fields':['comentarios']})

	]

class Comentario_TareaAdmin(admin.ModelAdmin):
	fieldsets = [
		('Tarea Comentada:', {'fields':['tarea']}),
		('Comento:', {'fields':['usuario']}),
		('Comentarios:', {'fields':['texto']})
	]

class ListaAdmin(admin.ModelAdmin):
	fieldsets = [
		('Lista del Curso:', {'fields':['curso']}),
		('Fecha de Asistencia', {'fields':['fecha']})
	]





# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Aviso, AvisoAdmin)
admin.site.register(Comentario_Aviso, Comentario_AvisoAdmin)
admin.site.register(Tarea, TareaAdmin)
admin.site.register(Entrega_Tarea, Entrega_TareaAdmin)
admin.site.register(Comentario_Tarea, Comentario_TareaAdmin)
admin.site.register(Lista, ListaAdmin)
admin.site.register(Asistencia)
admin.site.register(UserProfile)


