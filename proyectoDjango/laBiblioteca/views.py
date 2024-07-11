from django.contrib import messages
from django.contrib.auth import logout, login,authenticate 
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from . import forms
from .cart import Cart
from .forms import AltaLectoresForm, IngresoLectoresForm, UsuarioStaffForm, UsuarioForm, LibroForm, ContactosForm
from .models import Cliente, Libro, Venta, VentaLibro, User, Mensaje
import logging, os

# =================================== INICIO ====================================

def index(request):
    return render(request, 'laBiblioteca/index.html')

# ==================================== LOGIN ====================================

def ingresar(request):
    if request.method == 'GET':
        return render(request, 'laBiblioteca/ingresar.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'laBiblioteca/ingresar.html', {
                'form': AuthenticationForm, 
                'error': 'usuario o contraseña incorrectos'
                })
        else:
            login(request, user)

            return redirect('index')

# =================================== LOGOUT ====================================

def user_logout(request):
    logout(request)

    messages.success(request, 'Sesión cerrada')

    return redirect('index')

# ============================== REGISTRO USUARIO ===============================

def registro(request):
    if request.method =="GET":
        form = forms.AltaLectoresForm()
    else:
        form = AltaLectoresForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, '¡Te has dado de alta con éxito!')

            return redirect('login')

    return render(request, 'laBiblioteca/registro.html', {'alta_lector_form': form})

# ============================= CATALOGO DE LIBROS ==============================

class CatalogoLibros(ListView):
    model = Libro
    context_object_name = 'libros'
    template_name = 'laBiblioteca/catalogo.html'
    ordering = ['titulo']

# =================================== CARRITO ===================================

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

# ============================== PROCESO DE VENTA ===============================

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

# ============================ MENSAJES DE CONTACTOS ============================

def contactos(request):
    contexto = {}

    if request.method == "GET":
        contexto['contactos_form'] = forms.ContactosForm()
    else:
        form = forms.ContactosForm(request.POST)
        contexto['contactos_form'] = form

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

    return render(request, 'laBiblioteca/contactos.html', contexto)

# ================================ ADMIN LIBROS =================================

def panel_usuario(request):
    libros = Libro.objects.all()
    usuarios = User.objects.filter(is_staff=False)
    mensajes = Mensaje.objects.all()
    datos = {'libros': libros, 'usuarios': usuarios, 'mensajes' : mensajes}
    return render(request, 'laBiblioteca/panel_usuario.html', datos)

# =============================== USUARIO PERFIL ================================

def perfil(request):
    usuarios = User.objects.filter(is_staff=False)
    mensajes = Mensaje.objects.all()

    context = {'usuarios':usuarios, 'mensajes':mensajes}

    #if request.method == "GET":
        #context['perfil_form'] = forms.PerfilForm()
    #else:
        #form = forms.PerfilForm(request.POST)

        #context['perfil_form'] = form

        #if form.is_valid():
            #messages.success(request, 'El perfil se actualizo con éxito.')

           # return redirect('index')

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

# =============================== CRUD DE LIBROS ================================

class CrearLibroView(LoginRequiredMixin, CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'laBiblioteca/crear_libro.html'
    success_url = reverse_lazy('libros')

class EliminarLibroView(LoginRequiredMixin, DeleteView):
    model = Libro
    template_name = 'laBiblioteca/eliminar_libro.html'
    success_url = reverse_lazy('libros')

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
    success_url = reverse_lazy('libros')

    def form_valid(self, form):
        messages.success(self.request, 'Has modificado el libro con éxito')
        return super().form_valid(form)
