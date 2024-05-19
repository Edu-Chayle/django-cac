from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from . import forms
from .forms import AltaLectoresForm, IngresoLectoresForm

def index(request):
    return render(request, 'laBiblioteca/index.html')

def registro(request):
    contexto = {}
    if request.method =="GET":
        contexto['alta_lector_form'] = forms.AltaLectoresForm()
    else: #asumo que es un POST
        contexto['alta_alumno_form'] = forms.AltaLectoresForm(request.POST)
        #validar el form
        #si el form es correcto
        #si el form es correcto lo reirijo
        #si el form contiene errores, envio un mensaje de error
        #si todo esta OK; hago un comit en la base de datos
        redirect('index')
        print(request.POST)
        
    return render(request, 'laBiblioteca/registro.html', contexto)   
    
    
    


def ingresar(request):
    contexto = {}
    if request.method =="GET":
        contexto['ingreso_lector_form'] = forms.IngresoLectoresForm()
    else: #asumo que es un POST
        contexto['ingreso_lector_form'] = forms.IngresoLectoresForm(request.POST)
        #validar el form
        #si el form es correcto
        #si el form es correcto lo reirijo
        #si el form contiene errores, envio un mensaje de error
        #si todo esta OK; hago un comit en la base de datos
        redirect('index')
        print(request.POST)
    
    
    return render(request, 'laBiblioteca/ingresar.html', contexto)


def catalogo(request):
    return render(request, 'laBiblioteca/catalogo.html')

def contactos(request):
    contexto = {}
    if request.method =="GET":
        contexto['contactos_form'] = forms.ContactosForm()
    else: #asumo que es un POST
        contexto['contactos_form'] = forms.ContactosForm(request.POST)
        #validar el form
        #si el form es correcto
        #si el form es correcto lo reirijo
        #si el form contiene errores, envio un mensaje de error
        #si todo esta OK; hago un comit en la base de datos
        redirect('index')
        print(request.POST)
        
    return render(request, 'laBiblioteca/contactos.html', contexto)

def panel_usuario(request):
    return render(request, 'laBiblioteca/panel_usuario.html')
