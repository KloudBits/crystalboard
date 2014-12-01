# encoding: utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from Main.models import UserProfile, Curso, Clase, Capitulo, Quiz_Respuesta, Quiz_Aplicar, Quiz, Quiz_Pregunta, Entrega_Tarea, Tarea, Recurso

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'perfiles'

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Curso)
admin.site.register(Capitulo)
admin.site.register(Clase)

admin.site.register(Quiz)
admin.site.register(Quiz_Pregunta)
admin.site.register(Quiz_Respuesta)
admin.site.register(Quiz_Aplicar)
admin.site.register(Entrega_Tarea)
admin.site.register(Tarea)
admin.site.register(Recurso)
