from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CategoriaProducto, Producto
from .forms import ProductFrom
from django.contrib.auth.decorators import login_required

def index(request):
  context = {}
  return render(request,'taller/index.html', context)

def about(request):
  context = {}
  return render(request,'taller/about.html', context)

def contacto(request):
  context = {}
  return render(request,'taller/contact.html', context)

def productos(request):
  context = {}
  try:
    context.update({"alert":request.session["alert"]})
    del request.session["alert"]
  except KeyError:
    pass

  qs_categorias = CategoriaProducto.objects.all()
  qs_productos = Producto.objects.all()

  catalogo = {}
  for c in qs_categorias:
    lista_productos = qs_productos.filter(categoria = c)
    if lista_productos: catalogo[c.nombre] = lista_productos
  context.update({"catalogo":catalogo}) 
  return render(request,'productos/productos.html', context)

@login_required
def agregar_producto(request):
  if request.method == 'GET':
    form = ProductFrom()
    context = {"form": form}
  elif request.method == 'POST':
    form = ProductFrom(request.POST)
    if (form.is_valid()):
      form.save()
      alert = create_alert("success", "El producto fue agregado correctamente!")
    else:
      alert = {"type":"danger", "message":"Error al agregar el producto"}
    context = {"form": form, "alert":alert}
  return render(request, 'productos/formulario_producto.html' , context)

@login_required
def eliminar_producto(request,pk):
  if not (request.user.is_staff or request.user.is_authenticated):
    alert = create_alert("warning","Advertencia: No tienes permisos para realizar esta acción")
    request.session["alert"] = alert
    return redirect('taller-productos')
  obj = Producto.objects.get(pk=pk)
  try:
    obj.delete()
  except Exception as e:
    alert = create_alert("error",f"Error al borrar objeto: {e}")
  alert = create_alert("success", "El producto fue eliminado con éxito!")
  request.session["alert"] = alert
  return redirect('taller-productos')

@login_required
def editar_producto(request, pk):
  context={"editar":True}
  
  if not request.user.is_staff:
    request.session["alert"] = create_alert("warning","Advertencia: No tienes permisos para realizar esta acción")
    return redirect('taller-productos')
  
  # Buscar objeto
  try:
    obj = Producto.objects.get(pk=pk)
  except Exception as e:
    request.session["alert"] = create_alert("danger",f"Error al buscar producto: {e}")
    return redirect('taller-productos')
  
  if request.method == 'POST':
    form = ProductFrom(request.POST, instance=obj)
    if (form.is_valid()):
      form.save()
      alert = create_alert("success", "El producto fue editado correctamente!")
    else:
      alert = create_alert("danger", "error al editar producto...")
    context.update({"form":form, "alert":alert}) 
    return render(request,'productos/formulario_producto.html', context)
  
  form = ProductFrom(instance=obj)
  context.update({"form":form})
  return render(request, "productos/formulario_producto.html" , context)

def create_alert(type,message):
  return {"type": type, "message": message}
