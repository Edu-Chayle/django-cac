from django.contrib import admin
from .models import Cliente, Libro, Venta, VentaLibro

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'direccion')

class LibroAdmin(admin.ModelAdmin):
    list_display = ('isbn', 'portada', 'titulo', 'autor', 'precio', 'stock')

class VentaAdmin(admin.ModelAdmin):
    list_display = ('factura', 'fecha_venta', 'cliente', 'monto_total')

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Venta, VentaAdmin)
admin.site.register(VentaLibro)
