from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'laBiblioteca/index.html')

def registro(request):
    return render(request, 'laBiblioteca/registro.html')

def ingresar(request):
    return render(request, 'laBiblioteca/ingresar.html')
