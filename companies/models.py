from django.db import models

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
    