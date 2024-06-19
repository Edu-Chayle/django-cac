from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Cliente(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    apellido = models.CharField(max_length=50, verbose_name="Apellido")
    email = models.EmailField(verbose_name="Email", unique=True)
    direccion = models.CharField(max_length=50, verbose_name="Dirección")

    def __str__(self):
        return f"Nombre completo: {self.nombre} {self.apellido} - Email: {self.email} - Dirección: {self.direccion}"

class Libro(models.Model):
    isbn = models.CharField(max_length=13, verbose_name="ISBN", unique=True)
    portada = models.ImageField(upload_to="portadas/", blank=True, null=True, verbose_name="Portada")
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
