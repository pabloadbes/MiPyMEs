from django.db import models
from questions.models import Option

class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name="Razón Social")
    cuit = models.CharField(max_length=13, verbose_name="CUIT", default="")
    clanae_code = models.CharField(max_length=6, verbose_name="CLANAE")
    address_street = models.CharField(max_length=100, verbose_name="Calle / Ruta")
    address_number = models.CharField(max_length=100, verbose_name="Número / Km")
    city = models.CharField(max_length=100, verbose_name="Localidad")
    district = models.CharField(max_length=100, verbose_name="Departamento")
    zip_code = models.CharField(max_length=4, verbose_name="Código Postal")
    phone = models.CharField(max_length=12, verbose_name="Teléfono")
    email = models.EmailField(verbose_name="Correo")
    created = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Fecha de última modificación", auto_now=True)

    class Meta:
        verbose_name = "empresa"
        verbose_name_plural = "empresas"
        ordering = ["name", "created"]
    
    def __str__(self) -> str:
        return self.name
    
class Response(models.Model):
    value = models.CharField(verbose_name="Valor", max_length=500)
    company = models.ForeignKey(Company, verbose_name="Empresa", on_delete=models.SET_DEFAULT, default=0)
    option = models.ForeignKey(Option, verbose_name="Opción", on_delete=models.SET_DEFAULT, default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "encuesta"
        verbose_name_plural = "encuestas"
        ordering = ['company', '-updated']

    def __str__(self):
        return self.company.name