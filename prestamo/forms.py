from django import forms
from .models import Prestamo

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['empleado', 'tipo_prestamo', 'fecha_prestamo', 'monto', 'numero_cuotas']
        widgets = {
            'fecha_prestamo': forms.DateInput(attrs={'type': 'date'}),
        }