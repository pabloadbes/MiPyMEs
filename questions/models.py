from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Survey_Type(models.Model):
    name = models.CharField(verbose_name="nombre")
    year = models.IntegerField(verbose_name="año")
    description = models.CharField(max_length=500, verbose_name="Descripción")
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="survey_type_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="survey_type_updated_by_user")

    class Meta:
        verbose_name = "Tipo de pregunta"
        verbose_name_plural = "Tipos de pregunta"
        ordering = ["name"]
    
    def __str__(self) -> str:
        return self.name + " " + str(self.year)
    
    def get_description(self) -> str:
        return self.description
    
class Section(models.Model):
    section_order = models.CharField(max_length=2, verbose_name="Orden")
    text = models.CharField(max_length=200, verbose_name="Texto")
    survey_type = models.ForeignKey(Survey_Type, verbose_name="Tipo de Encuesta", on_delete=models.SET_DEFAULT, default=1)
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="section_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="section_updated_by_user")

    class Meta:
        verbose_name = "sección"
        verbose_name_plural = "secciones"
        ordering = ["section_order"]
    
    def __str__(self) -> str:
        return self.text
    
class Subsection(models.Model):
    text = models.CharField(max_length=500, verbose_name="Texto")
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="subtitle_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="subtitle_updated_by_user")

    class Meta:
        verbose_name = "subtítulo"
        verbose_name_plural = "subtítulos"
        ordering = ["-updated_at"]
    
    def __str__(self) -> str:
        return self.text
    
class Question_Type(models.Model):
    name = models.CharField(verbose_name="nombre")
    description = models.CharField(max_length=500, verbose_name="Descripción")
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="question_type_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="question_type_updated_by_user")

    class Meta:
        verbose_name = "Tipo de pregunta"
        verbose_name_plural = "Tipos de pregunta"
        ordering = ["name"]
        
    def __str__(self) -> str:
        return self.name
        
class Question(models.Model):
    number = models.IntegerField(verbose_name="Número")
    text = models.CharField(verbose_name="Contenido", max_length=500)
    question_type = models.ForeignKey(Question_Type, verbose_name="Tipo", on_delete=models.SET_DEFAULT, default=0)
    section = models.ForeignKey(Section, verbose_name="Secciones", on_delete=models.SET_DEFAULT, default=0)
    subsection = models.ForeignKey(Subsection, verbose_name="Subtítulo", on_delete=models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="question_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="question_updated_by_user")

    class Meta:
        verbose_name = "pregunta"
        verbose_name_plural = "preguntas"
        ordering = ['number']

    def __str__(self):
        return self.text
    
    def __type__(self):
        return self.type.name
    
    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"pk": self.pk})
    

class Item(models.Model):
    item_order = models.IntegerField(verbose_name="Orden")
    text = models.CharField(max_length=500, verbose_name="Texto")
    question = models.ForeignKey(Question, verbose_name="Pregunta", on_delete=models.SET_DEFAULT, default=0)
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="item_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="item_updated_by_user")

    class Meta:
        verbose_name = "ítem"
        verbose_name_plural = "ítems"
        ordering = ["item_order"]
    
    def __str__(self) -> str:
        return self.text

class Option(models.Model):
    option_order = models.IntegerField(verbose_name="Orden")
    text = models.CharField(max_length=500, verbose_name="Texto")
    item = models.ForeignKey(Item, verbose_name="Item", on_delete=models.SET_DEFAULT, default=0)
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="option_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="option_updated_by_user")

    class Meta:
        verbose_name = "opción"
        verbose_name_plural = "opciones"
        ordering = ["option_order"]
    
    def __str__(self) -> str:
        return self.text
    
class Note(models.Model):
    note_order = models.IntegerField(verbose_name="Orden")
    text = models.CharField(max_length=500, verbose_name="Texto")
    option = models.ForeignKey(Option, verbose_name="Option", on_delete=models.SET_DEFAULT, default=1)
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="note_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="note_updated_by_user")

    class Meta:
        verbose_name = "nota"
        verbose_name_plural = "notas"
        ordering = ["note_order"]
    
    def __str__(self) -> str:
        return self.text
    

