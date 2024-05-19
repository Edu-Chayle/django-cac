from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from . import forms
from .forms import AltaLectoresForm, IngresoLectoresForm
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


def catalogo(request):
    return render(request, 'laBiblioteca/catalogo.html')

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
