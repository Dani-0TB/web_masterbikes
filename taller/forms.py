from django import forms
from .models import CategoriaProducto, Producto
from django.utils.translation import gettext_lazy as _

class ProductFrom(forms.ModelForm):
  template_name = "productos/forms/form_producto.html"
  class Meta:
    model = Producto
    fields = ["nombre", "precio", "categoria", "descripcion"]
    widgets={
      "nombre": forms.TextInput(attrs={"class":"form-control mb-3 flex-grow"}),
      "precio": forms.NumberInput(attrs={"class":"form-control mb-3","min":1, "max":9999999999}),
      "categoria": forms.Select(attrs={"class":"form-select mb-3"}),
      "descripcion": forms.Textarea(attrs={"class":"form-control mb-3"}),
    }
  def __init__(self, *args, **kwargs):
    kwargs.setdefault('label_suffix', '')
    super(ProductFrom, self).__init__(*args, **kwargs)