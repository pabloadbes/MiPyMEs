from django.db import models
from django.contrib.auth.models import User
from team.models import Surveyor

class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name="Razón Social")
    cuit = models.CharField(max_length=13, verbose_name="CUIT", default="")
    clanae_code = models.CharField(max_length=6, verbose_name="CLANAE")
    surveyor = models.ForeignKey(Surveyor, verbose_name="Encuestador Asignado", on_delete=models.DO_NOTHING, blank=True, null=True)
    address_street = models.CharField(max_length=100, verbose_name="Calle / Ruta")
    address_number = models.CharField(max_length=100, verbose_name="Número / Km")
    city = models.CharField(max_length=100, verbose_name="Localidad")
    district = models.CharField(max_length=100, verbose_name="Departamento")
    zip_code = models.CharField(max_length=4, verbose_name="Código Postal")
    phone = models.CharField(max_length=12, verbose_name="Teléfono")
    email = models.EmailField(verbose_name="Correo")
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="company_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="company_updated_by_user")

    class Meta:
        verbose_name = "empresa"
        verbose_name_plural = "empresas"
        ordering = ["name", "created_at"]
    
    def __str__(self) -> str:
        return self.name
    