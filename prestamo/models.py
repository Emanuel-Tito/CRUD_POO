from decimal import Decimal
from django.db import models

from nomina.models import Empleado

# Create your models here.
class TipoPrestamo(models.Model):
    descripcion = models.CharField(max_length=100)
    tasa = models.IntegerField(default=0)
    
    def __str__(self):
        return self.descripcion

class Prestamo(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo_prestamo = models.ForeignKey(TipoPrestamo, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    interes = models.DecimalField(max_digits=10, decimal_places=2)
    monto_pagar = models.DecimalField(max_digits=10, decimal_places=2)
    numero_cuotas = models.PositiveIntegerField(default=1)
    cuota_mensual = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    

    def __str__(self):
        return f"Préstamo de {self.empleado.nombre} - {self.tipo_prestamo.descripcion}"
    
    def calcular_campos(self):
        tasa_decimal = Decimal(self.tipo_prestamo.tasa) / Decimal(100)
        self.interes = (self.monto * tasa_decimal).quantize(Decimal('0.01'))
        self.monto_pagar = (self.monto + self.interes).quantize(Decimal('0.01'))
        self.cuota_mensual = (self.monto_pagar / Decimal(self.numero_cuotas)).quantize(Decimal('0.01'))
        if self._state.adding and not self.saldo:
            # saldo inicial igual al monto_pagar
            self.saldo = self.monto_pagar
        else:
            # si se está editando y saldo no fue manualmente ajustado, mantener coherencia mínima
            self.saldo = self.saldo if self.saldo else self.monto_pagar

    def save(self, *args, **kwargs):
        self.calcular_campos()
        super().save(*args, **kwargs)