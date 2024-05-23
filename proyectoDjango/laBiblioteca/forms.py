from django import forms
from django.core.exceptions import ValidationError
import re

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

class PerfilForm(forms.Form):
    nombre = forms.CharField(max_length=50, label="Nombre", required=True)
    apellido = forms.CharField(max_length=50, label="Apellido", required=True)
    email = forms.EmailField(label="Email", required=True)
    contrasenia = forms.CharField(min_length=8, max_length=162, label="Contraseña", required=True, 
                                  widget=forms.PasswordInput, 
                                  help_text="Mínimo 8 caracteres, con al menos una letra minúscula, una letra \
                                             mayúscula y un número.")
    descripcion = forms.CharField(max_length=255, label="Descripción", required=False)

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if not nombre.isalpha():
            raise forms.ValidationError("El nombre solo debe contener letras.")

        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')

        if not apellido.isalpha():
            raise forms.ValidationError("El apellido solo debe contener letras.")

        return apellido

    """def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("El email ya se encuentra registrado.")

        return email"""

    def clean_contrasenia(self):
        re_contrasenia = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{,}$"
        contrasenia = self.cleaned_data.get('contrasenia')

        if not re.match(re_contrasenia, contrasenia):
            raise forms.ValidationError("La contraseña no es válida.")

        return contrasenia
