from django.db import models
from companies.models import Company
from questions.models import Option

class Survey(models.Model):
    company = models.ForeignKey(Company, verbose_name="Empresa", on_delete=models.SET_DEFAULT, default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "encuesta"
        verbose_name_plural = "encuestas"
        ordering = ['-updated', 'company']

    def __str__(self):
        return self.company.name
        # return self.company.__str__(self.company)
        # return self.company.__str__(company.self)

class Response(models.Model):
    value = models.CharField(verbose_name="Valor", max_length=500)
    survey = models.ForeignKey(Survey, verbose_name="Empresa", on_delete=models.SET_DEFAULT, default=0)
    option = models.ForeignKey(Option, verbose_name="Opción", on_delete=models.SET_DEFAULT, default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "respuesta"
        verbose_name_plural = "respuestas"
        ordering = ['survey', '-updated']

    def __str__(self):
        return self.survey.company.name