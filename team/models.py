from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Supervisor(models.Model):
   user = models.OneToOneField(User, verbose_name="Usuario", on_delete=models.CASCADE)
   SUP_CODE = models.IntegerField(verbose_name="Código de Supervisor")
   created = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
   updated = models.DateTimeField(verbose_name="Fecha de última modificación", auto_now=True)

   class Meta:
      verbose_name = "supervisor"
      verbose_name_plural = "supervisores"
      ordering = ['SUP_CODE']

   def __str__(self):
      return " ".join([self.user.first_name, self.user.last_name])

class Surveyor(models.Model):
   user = models.OneToOneField(User, verbose_name="Usuario", on_delete=models.CASCADE)
   ENC_CODE = models.IntegerField(verbose_name="Código de Encuestador")
   supervisor = models.ForeignKey(Supervisor, verbose_name="Supervisor", on_delete=models.CASCADE)
   created = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
   updated = models.DateTimeField(verbose_name="Fecha de última modificación", auto_now=True)

   class Meta:
      verbose_name = "encuestador"
      verbose_name_plural = "encuestadores"
      ordering = ['ENC_CODE']

   def __str__(self):
      return " ".join([self.user.first_name, self.user.last_name])
