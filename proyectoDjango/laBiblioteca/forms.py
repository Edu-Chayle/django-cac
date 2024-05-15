from django import forms

class AltaLectoresForm(forms.Form):
    nombre = forms.CharField(label="Nombre", required=True)
    apellido = forms.CharField(label="Apellido", required=True)
    dni = forms.IntegerField(label="DNI", required=True)
    email = forms.EmailField(label="Email", required=True)
    contraseña = forms.CharField(label="Contraseña", required=True)
    repetirContraseña = forms.CharField(label="Repita su Contraseña", required=True)
    direccion = forms.CharField(label="Dirección", required=True)
    
    
    
    
class IngresoLectoresForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)
    contraseña = forms.CharField(label="Contraseña", required=True)