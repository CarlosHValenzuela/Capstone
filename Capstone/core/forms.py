from django import forms
from .models import Persona, Auto

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'edad', 'telefono', 'correo', 'direccion', 'tipo', 'activo']
        
class AutoForm(forms.ModelForm):
    class Meta:
        model = Auto
        fields = ['placa', 'marca', 'persona']