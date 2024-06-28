from django.db.models import Max
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from . import forms
from .cart import Cart
from .forms import AltaLectoresForm, IngresoLectoresForm, UsuarioStaffForm, UsuarioForm, LibroForm, ContactosForm
from .models import Cliente, Libro, Venta, VentaLibro, User, Mensaje
from django.contrib import messages
from django.views.generic.list import ListView
from django.contrib.auth import logout, login
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, DeleteView
import os, logging
#configurando path para CRUD de libros
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Libro
from .forms import LibroForm


def index(request):
    return render(request, 'laBiblioteca/index.html')

class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        if user.is_staff:
            return redirect('index')
        else:
            return redirect('panel_usuario')
        
def user_logout(request):
    logout(request)

    messages.success(request, 'Sesion Cerrada')

    return redirect('index')


def registro(request):
    contexto = {}
    if request.method =="GET":
        form = forms.AltaLectoresForm()  
    else:
        form = AltaLectoresForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Te has dado de alta con éxito!')
            
            return redirect('login')
        else:
            return render(request, 'laBiblioteca/registro.html', {'alta_lector_form': form})

    
    
    return render(request, 'laBiblioteca/registro.html', {'alta_lector_form': form})


def ingresar(request):
    contexto = {}
    if request.method =="GET":
        contexto['ingreso_lector_form'] = forms.IngresoLectoresForm()
    else: #asumo que es un POST
        form = IngresoLectoresForm(request.POST)
        contexto['ingreso_lector_form'] = forms.IngresoLectoresForm(request.POST)
        #validar el form
        #validar el form
        # if form.is_valid():
        #     #si el form es correcto
        #     #si el form es correcto lo reirijo
        #     print(request.POST)
            
        #     return redirect('panel_usuario')
        #si el form es correcto
        #si el form es correcto lo reirijo
        #si el form contiene errores, envio un mensaje de error
        #si todo esta OK; hago un comit en la base de datos
        print(request.POST)
        return redirect('panel_usuario')

    return render(request, 'laBiblioteca/ingresar.html', contexto)

class CatalogoLibros(ListView):
    model = Libro
    context_object_name = 'libros'
    template_name = 'laBiblioteca/catalogo.html'
    ordering = ['titulo']

def agregar_al_carrito(request, libro_id):
    libro = get_object_or_404(Libro, id = libro_id)
    cart = Cart(request)

    cart.add_to_cart(libro)

    return redirect(request.META.get('HTTP_REFERER'))

def quitar_del_carrito(request, libro_id):
    cart = Cart(request)

    cart.remove_from_cart(libro_id)

    return redirect(request.META.get('HTTP_REFERER'))

def clear_cart(request):
    cart = Cart(request)

    cart.clear_cart()

    return redirect('carrito')

def carrito(request):
    cart = Cart(request)
    total_price = cart.get_total_price()

    return render(request, 'laBiblioteca/carrito.html', {'cart': cart, 'total_price': total_price})

logger = logging.getLogger(__name__)

# Volvi el carrito a la version funcional, cree generar_numero_factura y modifique venta

def generar_numero_factura():
    last_invoice = Venta.objects.aggregate(Max('factura'))['factura__max']
    if last_invoice:
        new_number = int(last_invoice) + 1
    else:
        new_number = 1

    return str(new_number).zfill(10)

def venta(request):
    cliente = get_object_or_404(Cliente, email=request.user.email)
    cart = Cart(request)

    nueva_factura = generar_numero_factura()

    nueva_venta = Venta.objects.create(
        factura=nueva_factura,
        cliente=cliente,
        monto_total=cart.get_total_price()
    )

    for libro_id, item in cart.cart.items():
        libro = get_object_or_404(Libro, id=libro_id)

        if libro.stock >= item['cantidad']:
            libro.stock -= item['cantidad']
            libro.save()
        else:
            raise ValidationError(f"No hay suficiente stock para el libro {libro.titulo} (ISBN: {libro.isbn})")

        VentaLibro.objects.create(
            venta=nueva_venta,
            libro=libro,
            cantidad=item['cantidad'],
            precio_unitario=item['precio']
        )

    cart.clear_cart()

    return redirect('index')

def contactos(request):
    contexto = {}
    if request.method == "GET":
        contexto['contactos_form'] = forms.ContactosForm()
    else:  # asumo que es un POST
        form = forms.ContactosForm(request.POST)
        contexto['contactos_form'] = form
        # validar el form
        if form.is_valid():
            nuevo_mensaje = Mensaje(
                nombre=form.cleaned_data['nombre'],
                email=form.cleaned_data['email'],
                mensaje=form.cleaned_data['mensaje'],
                recibir_noticias=form.cleaned_data['recibir_noticias']
            )
            nuevo_mensaje.save()
            messages.success(request, '¡Tu mensaje ha sido enviado con éxito!')
            return redirect('contactos')
    
    # Renderizar el formulario con los datos de contexto
    return render(request, 'laBiblioteca/contactos.html', contexto)

def panel_usuario(request):
    libros = Libro.objects.all()
    usuarios = User.objects.filter(is_staff=False)
    mensajes = Mensaje.objects.all()
    datos = {'libros': libros, 'usuarios': usuarios, 'mensajes' : mensajes}
    return render(request, 'laBiblioteca/panel_usuario.html', datos)

def perfil(request):
    context = {}

    if request.method == "GET":
        context['perfil_form'] = forms.PerfilForm()
    else:
        form = forms.PerfilForm(request.POST)

        context['perfil_form'] = form

        if form.is_valid():
            messages.success(request, 'El perfil se actualizo con éxito.')

            return redirect('index')

    return render(request, 'laBiblioteca/perfil.html', context)


class mis_datos(ListView):
    model = User
    context_object_name = 'User'
    template_name = 'laBiblioteca/mis_datos.html'
    ordering = ['id']
    
    
class ModificarUsuarioView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'laBiblioteca/modificar_usuario.html'

    def get_form_class(self):
        if self.request.user.is_staff:
            return UsuarioStaffForm
        else:
            return UsuarioForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Has modificado tus datos con éxito.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('panel_usuario')
    
    
    
class EliminarLibroView(LoginRequiredMixin, DeleteView):
    model = Libro
    template_name = 'laBiblioteca/eliminar_libro.html'
    success_url = reverse_lazy('panel_usuario')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.imagen and self.object.imagen.name != 'imagenes_bd/sin_foto.webp':
            if os.path.isfile(self.object.imagen.path):
                os.remove(self.object.imagen.path)
        messages.success(request, 'Has eliminado el libro con éxito')
        return super().delete(request, *args, **kwargs)
    
class ActualizarLibroView(LoginRequiredMixin, UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'laBiblioteca/actualizar_libro.html'
    success_url = reverse_lazy('panel_usuario')

    def form_valid(self, form):
        messages.success(self.request, 'Has modificado el libro con éxito')
        return super().form_valid(form)

#configurando el CRUD de libros creacion de vistas
class LibroListView(ListView):
    model = Libro
    template_name = 'libro_list.html'

class LibroDetailView(DetailView):
    model = Libro
    template_name = 'libro_detail.html'

class LibroCreateView(CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libro_form.html'

class LibroUpdateView(UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libro_form.html'

class LibroDeleteView(DeleteView):
    model = Libro
    template_name = 'libro_confirm_delete.html'
    success_url = reverse_lazy('libro_list')


