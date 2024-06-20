from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator

class Persona(models.Model):
    usuario = models.CharField(
        max_length=150,
        verbose_name="Usuario",
        unique=True,
        validators=[UnicodeUsernameValidator],
        null=True,
        blank=True
    )
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    dni = models.IntegerField(verbose_name="DNI", unique=True, null=True, blank=True)
    email = models.EmailField(verbose_name="Email", unique=True, null=True, blank=True)

    class Meta:
        abstract = True

class Cliente(AbstractUser, Persona):
    password = models.CharField(max_length=128, verbose_name="Contraseña", null=True, blank=True)
    password2 = models.CharField(max_length=128, verbose_name="Repita su Contraseña", null=True, blank=True)
    direccion = models.CharField(max_length=50, verbose_name="Dirección", null=True, blank=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="cliente_set",
        related_query_name="cliente",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="cliente_set",
        related_query_name="cliente",
    )

    def save(self, *args, **kwargs):
        if not self.id and self.password:
            self.password = make_password(self.password)
        if not self.username:
            self.username = self.usuario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Nombre completo: {self.nombre} {self.apellido} - Email: {self.email} - Dirección: {self.direccion}"

class Libro(models.Model):
    isbn = models.CharField(max_length=13, verbose_name="ISBN", unique=True)
    portada = models.ImageField(upload_to="imagenes/", null=True, blank=True, verbose_name="Portada")
    titulo = models.CharField(max_length=50, verbose_name="Título")
    autor = models.CharField(max_length=50, verbose_name="Autor")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    stock = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], verbose_name="Stock")

    def __str__(self):
        return f"ISBN: {self.isbn} - Portada: {self.portada} - Título: {self.titulo} - Autor: {self.autor} - Precio: {self.precio} - Stock: {self.stock}"

class Venta(models.Model):
    factura = models.CharField(max_length=10, verbose_name="Factura", unique=True)
    fecha_venta = models.DateField(auto_now_add=True, verbose_name="Fecha venta")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="ventas")
    libros = models.ManyToManyField(Libro, through="VentaLibro")
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto total")

    def __str__(self):
        return f"Factura: {self.factura} - Fecha: {self.fecha_venta} - Cliente: {self.cliente} - Monto total: {self.monto_total}"

class VentaLibro(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)], verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio unitario")
    
    def __str__(self):
        return f"Factura: {self.venta.factura} - Libro: {self.libro.titulo} - Cantidad: {self.cantidad} - Precio unitario: {self.precio_unitario}"
    
class Mensaje(models.Model):
    nombre = models.CharField(max_length=160, verbose_name="Nombre")
    email = models.EmailField( verbose_name="Email", unique=False, null=False, blank=False,)
    mensaje = models.CharField(max_length=500, verbose_name="Mensaje")
    recibir_noticias = models.BooleanField(verbose_name="Suscribirse a noticias", blank=True)
    def __str__(self):
        return f"Nombre: {self.nombre} | Email: {self.email} | Mensaje: {self.mensaje} | Recibir noticias: {self.recibir_noticias}"   
