from django import forms
from django.core.exceptions import ValidationError

class AltaLectoresForm(forms.Form):
    nombre = forms.CharField(label="Nombre", required=True)
    apellido = forms.CharField(label="Apellido", required=True)
    dni = forms.IntegerField(label="DNI", required=True)
    email = forms.EmailField(label="Email", required=True)
    contraseña = forms.CharField(label="Contraseña", required=True)
    repetirContraseña = forms.CharField(label="Repita su Contraseña", required=True)
    direccion = forms.CharField(label="Dirección", required=True)
    
    def clean_nombre(self):
        if not self.cleaned_data["nombre"].isalpha():
            raise ValidationError("El nombre solo puede estar compuesto por letras")
        
        return self.cleaned_data["nombre"]
    
    def clean_apellido(self):
        if not self.cleaned_data["apellido"].isalpha():
            raise ValidationError("El apellido solo puede estar compuesto por letras")
        
        return self.cleaned_data["apellido"]
    
    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get("nombre")
        apellido = cleaned_data.get("apellido")
        contraseña = cleaned_data.get("contraseña")
        contraseña2 = cleaned_data.get("repetirContraseña")
        
        if nombre == "nombre" and apellido == "apellido":
            raise ValidationError("El usuario ya existe")
        
        if self.cleaned_data["dni"] < 1000000:
            raise ValidationError("ElDNI debe contener almenos 7 digitos")
        
        if not contraseña == contraseña2:
            raise ValidationError("Las contraseñas deben ser iguales")

        return self.cleaned_data    
    
    
    
class IngresoLectoresForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)
    contraseña = forms.CharField(label="Contraseña", required=True)
    
    
    
    
    
class ContactosForm(forms.Form):
    nombre = forms.CharField(label="Nombre", required=True)
    email = forms.EmailField(label="Email", required=True)
    mensaje = forms.CharField(label="Mensaje", required=True,widget=forms.Textarea(attrs={'class': 'textarea_contacto'}))
    recibir_noticias = forms.BooleanField(label="Suscribirse a noticias", required=False)
