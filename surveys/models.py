from django.db import models

class Survey(models.Model):
    company = models.ForeignKey(verbose_name="Empresa")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "encuesta"
        verbose_name_plural = "encuestas"
        ordering = ['-updates', 'empresa']

    def __str__(self):
        return self.company
        # return self.company.__str__(self.company)
        # return self.company.__str__(company.self)
