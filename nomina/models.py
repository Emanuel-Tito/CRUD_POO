from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

# Create your models here.

class Empleado(models.Model):
    cedula = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='La cédula debe tener exactamente 10 dígitos numéricos.'
            )
        ],
        help_text='Cédula ecuatoriana de 10 dígitos'
    )
    nombre = models.CharField(max_length=100)
    sueldo = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0, 'El sueldo no puede ser negativo.')])
    departamento = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.nombre} ({self.cedula})"

class Nomina(models.Model):
    aniomes = models.CharField(max_length=6)
    tot_ing = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tot_des = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    neto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Nómina {self.aniomes}"
    
    def calcular_totales(self):
        detalles = self.nominadetalle_set.all()
        self.tot_ing = sum(detalle.tot_ing for detalle in detalles)
        self.tot_des = sum(detalle.tot_des for detalle in detalles)
        self.neto = sum(detalle.neto for detalle in detalles)
        self.save()

class NominaDetalle(models.Model):
    nomina = models.ForeignKey(Nomina, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    sueldo = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'), _('El sueldo no puede ser negativo.'))]
    )
    bono = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'), _('El bono no puede ser negativo.'))]
    )
    tot_ing = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iess = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prestamo = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'), _('El préstamo no puede ser negativo.'))]
    )
    tot_des = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    neto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def save(self, *args, **kwargs):
        # Calcular total ingresos
        self.tot_ing = self.sueldo + self.bono
        
        # Calcular IESS (9.45% del sueldo) - Usar Decimal correctamente
        porcentaje_iess = Decimal('0.0945')  # 9.45% como Decimal
        self.iess = self.sueldo * porcentaje_iess
        
        # Calcular total descuentos
        self.tot_des = self.iess + self.prestamo
        
        # Calcular neto
        self.neto = self.tot_ing - self.tot_des
        
        super().save(*args, **kwargs)
        
        # Recalcular totales de la nómina
        self.nomina.calcular_totales()
    
    def __str__(self):
        return f"{self.empleado.nombre} - {self.nomina.aniomes}"