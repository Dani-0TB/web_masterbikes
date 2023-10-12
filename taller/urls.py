from django.urls import path

from . import views

urlpatterns = [
  path("", views.index, name="taller-index"),
  path("about/", views.about, name="taller-about"),
  path("contacto/", views.contacto, name="taller-contacto"),
  path("productos/", views.productos, name="taller-productos"),
  path("productos/agregar/", views.agregar_producto, name="productos-agregar"),
  path("productos/editar/<int:pk>", views.editar_producto, name="productos-editar"),
  path("productos/eliminar/<int:pk>", views.eliminar_producto, name='productos-eliminar')
]