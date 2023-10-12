from django.db import models

class CategoriaProducto(models.Model):
  nombre = models.CharField(max_length=60)

  def __str__(self):
    return self.nombre

class Producto(models.Model):
  nombre = models.CharField(max_length=100)
  descripcion = models.TextField("Descripción",blank=True, default='Sin descripción')
  precio = models.IntegerField()
  categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE, verbose_name="Categoría")

  def __str__(self):
    return self.nombre

  class Meta:
    ordering = ["categoria", "nombre"]