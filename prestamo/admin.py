from django.contrib import admin
from .models import TipoPrestamo, Prestamo

@admin.register(TipoPrestamo)
class TipoPrestamoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'tasa')
    search_fields = ('descripcion',)

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'tipo_prestamo', 'fecha_prestamo', 'monto', 'interes', 'monto_pagar', 'numero_cuotas', 'cuota_mensual', 'saldo')
    list_filter = ('tipo_prestamo', 'fecha_prestamo')