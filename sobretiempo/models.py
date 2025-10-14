from django.db import models
from nomina.models import Empleado  # Ajusta si tu modelo está en otra app
from decimal import Decimal

class TipoSobretiempo(models.Model):
    codigo = models.CharField(max_length=10)  # Ej: "H50", "H100"
    descripcion = models.CharField(max_length=100)  # Ej: "Horas al 50%"
    factor = models.DecimalField(max_digits=4, decimal_places=2)  # Ej: 1.50

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Sobretiempo(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha_registro = models.DateField()
    tipo_sobretiempo = models.ForeignKey(TipoSobretiempo, on_delete=models.CASCADE)
    numero_horas = models.DecimalField(max_digits=6, decimal_places=2)
    valor = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def calcular_valor(self):
        horas_mensuales = Decimal(240)
        sueldo_mensual = self.empleado.sueldo  # Ajusta si el campo se llama distinto
        valor_hora = sueldo_mensual / horas_mensuales
        self.valor = (valor_hora * self.numero_horas * self.tipo_sobretiempo.factor).quantize(Decimal('0.01'))

    def save(self, *args, **kwargs):
        self.calcular_valor()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.empleado.nombre} - {self.fecha_registro} ({self.numero_horas}h)"