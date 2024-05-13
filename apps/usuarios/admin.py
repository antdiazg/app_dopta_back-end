from django.contrib import admin
from apps.usuarios.models import Persona, Administrador, Organizacion


admin.site.register(Persona)
admin.site.register(Administrador)
admin.site.register(Organizacion)
