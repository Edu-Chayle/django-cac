from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic.list import ListView
from . import forms
from .cart import Cart
from .forms import AltaLectoresForm, IngresoLectoresForm
from .models import Cliente, Libro, Venta, VentaLibro
from django.contrib import messages

def index(request):
    return render(request, 'laBiblioteca/index.html')

def registro(request):
    contexto = {}
    if request.method =="GET":
        contexto['alta_lector_form'] = forms.AltaLectoresForm()
    else: #asumo que es un POST
        form = AltaLectoresForm(request.POST)
        contexto['alta_lector_form'] = forms.AltaLectoresForm(request.POST)
        #validar el form
        if form.is_valid():
            #si el form es correcto
            #si el form es correcto lo reirijo
            messages.success(request, '¡Te has dado de alta con éxito!')
            print(request.POST)

            return redirect('ingresar')
        #si el form contiene errores, envio un mensaje de error
        #si todo esta OK; hago un comit en la base de datos

    return render(request, 'laBiblioteca/registro.html', contexto)   

def ingresar(request):
    contexto = {}
    if request.method =="GET":
        contexto['ingreso_lector_form'] = forms.IngresoLectoresForm()
    else: #asumo que es un POST
        form = AltaLectoresForm(request.POST)
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

def venta(request):
    cliente = get_object_or_404(Cliente, email=request.user.email)
    cart = Cart(request)

    nueva_venta = Venta.objects.create(
        factura="FACT" + str(timezone.now().timestamp()).replace('.', ''),
        cliente=cliente,
        monto_total=cart.get_total_price()
    )

    for libro_id, item in cart.cart.items():
        libro = get_object_or_404(Libro, id=libro_id)

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
    if request.method =="GET":
        contexto['contactos_form'] = forms.ContactosForm()
    else: #asumo que es un POST
        form = AltaLectoresForm(request.POST)
        contexto['contactos_form'] = forms.ContactosForm(request.POST)
        #validar el form
        #validar el form
        if form.is_valid():
            #si el form es correcto
            #si el form es correcto lo reirijo
            print(request.POST)

            redirect('index')
        #si el form es correcto
        #si el form es correcto lo reirijo
        #si el form contiene errores, envio un mensaje de error
        #si todo esta OK; hago un comit en la base de datos
        redirect('index')
        print(request.POST)

    return render(request, 'laBiblioteca/contactos.html', contexto)

def panel_usuario(request):
    return render(request, 'laBiblioteca/panel_usuario.html')

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
