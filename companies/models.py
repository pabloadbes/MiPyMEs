from django.db import models
from django.contrib.auth.models import User
from team.models import Surveyor, Supervisor

class State(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")
    #code = models.CharField(max_length=3, verbose_name="Código")
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="state_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="state_updated_by_user")

    class Meta:
        verbose_name = "provincia"
        verbose_name_plural = "provincias"
        ordering = ["name"]
    
    def __str__(self) -> str:
        return self.name

class District(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")
    #code = models.CharField(max_length=3, verbose_name="Código")
    state = models.ForeignKey(State, verbose_name="Provincia", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="district_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="district_updated_by_user")

    class Meta:
        verbose_name = "departamento"
        verbose_name_plural = "departamentos"
        ordering = ["name"]
    
    def __str__(self) -> str:
        return self.name

class City(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")
    code = models.IntegerField(verbose_name="Código")
    district = models.ForeignKey(District, verbose_name="Departamento", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="city_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="city_updated_by_user")

    class Meta:
        verbose_name = "localidad"
        verbose_name_plural = "localidades"
        ordering = ["name"]
    
    def __str__(self) -> str:
        return self.name
        

class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name="Razón Social")
    cuit = models.CharField(max_length=13, verbose_name="CUIT", default="")
    clanae_code = models.CharField(max_length=6, verbose_name="CLANAE")
    surveyor = models.ForeignKey(Surveyor, verbose_name="Encuestador Asignado", on_delete=models.DO_NOTHING, blank=True, null=True)
    supervisor = models.ForeignKey(Supervisor, verbose_name="Supervisor Asignado", on_delete=models.DO_NOTHING, blank=True, null=True)
    year = models.IntegerField(verbose_name="Año del operativo")
    due_id = models.IntegerField(verbose_name="Valor del campo ID en DUE")
    inactive = models.BooleanField(verbose_name="Estado")
    original_id = models.IntegerField(verbose_name="ID original")
    address_street = models.CharField(max_length=100, verbose_name="Calle / Ruta")
    address_number = models.CharField(max_length=100, verbose_name="Número / Km")
    city = models.ForeignKey(City, verbose_name="Localidad", on_delete=models.DO_NOTHING)
    district = models.ForeignKey(District, verbose_name="Departamento", on_delete=models.DO_NOTHING)
    zip_code = models.CharField(max_length=4, verbose_name="Código Postal")
    phone = models.CharField(max_length=12, verbose_name="Teléfono")
    email = models.EmailField(verbose_name="Correo")
    web_page = models.CharField(verbose_name="Página web")
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
    