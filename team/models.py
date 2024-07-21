from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User

# Create your models here.
class Supervisor(models.Model):
   user = models.OneToOneField(User, verbose_name="Usuario", on_delete=models.CASCADE)
   SUP_CODE = models.IntegerField(verbose_name="Código de Supervisor")
   created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
   updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
   created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="supervisor_created_by_user")
   updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="supervisor_updated_by_user")

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
   created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
   updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
   created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="surveyor_created_by_user")
   updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="surveyor_updated_by_user")

   class Meta:
      verbose_name = "encuestador"
      verbose_name_plural = "encuestadores"
      ordering = ['ENC_CODE']

   def __str__(self):
      return " ".join([self.user.first_name, self.user.last_name])
