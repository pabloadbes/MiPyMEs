from django.db import models
from django.urls import reverse

class Survey_Type(models.Model):
    name = models.CharField(verbose_name="nombre")
    description = models.CharField(max_length=500, verbose_name="Descripción")
    created = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Fecha de última modificación", auto_now=True)

    class Meta:
        verbose_name = "Tipo de pregunta"
        verbose_name_plural = "Tipos de pregunta"
        ordering = ["name"]
    
    def __str__(self) -> str:
        return self.name   
    
class Section(models.Model):
    section_order = models.CharField(max_length=2, verbose_name="Orden")
    text = models.CharField(max_length=200, verbose_name="Texto")
    survey_type = models.ForeignKey(Survey_Type, verbose_name="Tipo de Encuesta", on_delete=models.SET_DEFAULT, default=1)
    created = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Fecha de última modificación", auto_now=True)

    class Meta:
        verbose_name = "sección"
        verbose_name_plural = "secciones"
        ordering = ["section_order"]
    
    def __str__(self) -> str:
        return self.section_order + ": " + self.text
    
class Question_Type(models.Model):
    name = models.CharField(verbose_name="nombre")
    description = models.CharField(max_length=500, verbose_name="Descripción")
    created = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Fecha de última modificación", auto_now=True)

    class Meta:
        verbose_name = "Tipo de pregunta"
        verbose_name_plural = "Tipos de pregunta"
        ordering = ["name"]
        
    def __str__(self) -> str:
        return self.name
        
class Question(models.Model):
    question_order = models.CharField(verbose_name="Orden", max_length=10)
    number = models.IntegerField(verbose_name="Número")
    text = models.CharField(verbose_name="Contenido", max_length=500)
    question_type = models.ForeignKey(Question_Type, verbose_name="Tipo", on_delete=models.SET_DEFAULT, default=0)
    section = models.ForeignKey(Section, verbose_name="Secciones", on_delete=models.SET_DEFAULT, default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "pregunta"
        verbose_name_plural = "preguntas"
        ordering = ['question_order']

    def __str__(self):
        return self.question_order + ". " + self.text
    
    def __type__(self):
        return self.type.name
    
    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"pk": self.pk})
    

class Item(models.Model):
    item_order = models.IntegerField(verbose_name="Orden")
    text = models.CharField(max_length=500, verbose_name="Texto")
    question = models.ForeignKey(Question, verbose_name="Pregunta", on_delete=models.SET_DEFAULT, default=0)
    created = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Fecha de última modificación", auto_now=True)

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
    created = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Fecha de última modificación", auto_now=True)

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
    created = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Fecha de última modificación", auto_now=True)

    class Meta:
        verbose_name = "nota"
        verbose_name_plural = "notas"
        ordering = ["note_order"]
    
    def __str__(self) -> str:
        return self.text
    
class Subtitle(models.Model):
    text = models.CharField(max_length=500, verbose_name="Texto")
    question = models.ForeignKey(Question, verbose_name="Pregunta", on_delete=models.SET_DEFAULT, default=0)
    created = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Fecha de última modificación", auto_now=True)

    class Meta:
        verbose_name = "subtítulo"
        verbose_name_plural = "subtítulos"
        ordering = ["-updated"]
    
    def __str__(self) -> str:
        return self.text
