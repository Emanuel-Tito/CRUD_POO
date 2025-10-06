from django.contrib import admin
from .models import Nomina, NominaDetalle, Empleado

# Register your models here.
@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['cedula', 'nombre', 'sueldo', 'departamento', 'cargo']
    search_fields = ['cedula', 'nombre']

@admin.register(Nomina)
class NominaAdmin(admin.ModelAdmin):
    list_display = ['aniomes', 'tot_ing', 'tot_des', 'neto']
    list_filter = ['aniomes']

@admin.register(NominaDetalle)
class NominaDetalleAdmin(admin.ModelAdmin):
    list_display = ['nomina', 'empleado', 'sueldo', 'bono', 'neto']
    list_filter = ['nomina']