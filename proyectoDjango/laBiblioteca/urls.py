from  django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('registro', views.registro, name = 'registro'),
    path('ingresar', views.ingresar, name = 'ingresar'),
    path('catalogo', views.catalogo, name = 'catalogo'),
    path('contactos', views.contactos, name = 'contactos'),
    path('panel_usuario', views.panel_usuario, name = 'panel_usuario'),
    path('perfil', views.perfil, name='perfil'),
]


