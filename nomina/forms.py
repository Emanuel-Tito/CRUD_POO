from django import forms
from .models import Empleado, Nomina, NominaDetalle

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['cedula', 'nombre', 'sueldo', 'departamento', 'cargo']
        widgets = {
            'cedula': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]{10}',
                'title': '10 dígitos numéricos',
                'maxlength': '10'
            }),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'sueldo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01'
            }),
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
        }

class NominaForm(forms.ModelForm):
    class Meta:
        model = Nomina
        fields = ['aniomes']
        widgets = {
            'aniomes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYYMM (ej: 202501)'
            }),
        }

class NominaDetalleForm(forms.ModelForm):
    class Meta:
        model = NominaDetalle
        fields = ['empleado', 'sueldo', 'bono', 'prestamo']
        widgets = {
            'empleado': forms.Select(attrs={'class': 'form-control'}),
            'sueldo': forms.NumberInput(attrs={'class': 'form-control'}),
            'bono': forms.NumberInput(attrs={'class': 'form-control'}),
            'prestamo': forms.NumberInput(attrs={'class': 'form-control'}),
        }