from  django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('registro', views.registro, name = 'registro'),
    path('ingresar', views.ingresar, name = 'ingresar'),
    path('catalogo', views.CatalogoLibros.as_view(), name ='catalogo'),
    path('carrito/agregar/<int:libro_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/quitar/<int:libro_id>/', views.quitar_del_carrito, name='quitar_del_carrito'),
    path('carrito/vaciar', views.clear_cart, name='clear_cart'),
    path('contactos', views.contactos, name = 'contactos'),
    path('panel_usuario', views.panel_usuario, name = 'panel_usuario'),
    path('perfil', views.perfil, name='perfil'),
    path('carrito', views.carrito, name='carrito'),
]
