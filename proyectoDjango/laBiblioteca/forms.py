from django import forms
from django.core.exceptions import ValidationError
from .models import Cliente, User, Libro, Mensaje
import re

class AltaLectoresForm(forms.ModelForm):
    password2 = forms.CharField(label="Repita su Contraseña", widget=forms.PasswordInput, required=True)

    class Meta:
        model = Cliente
        fields = ['usuario', 'nombre', 'apellido', 'dni', 'email', 'password', 'password2', 'direccion']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', "Las contraseñas deben ser iguales")

        return cleaned_data

    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.set_password(self.cleaned_data["password"])

        #tabla auth_user
        user = User.objects.create_user(
            username=cliente.usuario,
            email=cliente.email,
            password=self.cleaned_data["password"],
            first_name=cliente.nombre,
            last_name=cliente.apellido
        )

        if commit:
            cliente.save()
        return cliente
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            raise ValidationError("El nombre solo puede estar compuesto por letras y espacios")
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get("apellido")
        if not re.match(r'^[a-zA-Z\s]+$', apellido):
            raise ValidationError("El apellido solo puede estar compuesto por letras y espacios")
        return apellido

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get("nombre")
        apellido = cleaned_data.get("apellido")
        contraseña = cleaned_data.get("contraseña")
        contraseña2 = cleaned_data.get("repetirContraseña")

        if not contraseña == contraseña2:
            raise ValidationError("Las contraseñas deben ser iguales")

        return self.cleaned_data    

class IngresoLectoresForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)
    contraseña = forms.CharField(label="Contraseña", required=True)

class ContactosForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = '__all__'
        widgets = {
            'mensaje': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }

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
    
    
class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['isbn', 'portada', 'titulo', 'autor', 'precio', 'stock']
        
        
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

class UsuarioStaffForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
