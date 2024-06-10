from django.db import models

class Section(models.Model):
    section_order = models.CharField(max_length=2, verbose_name="Orden")
    text = models.CharField(max_length=200, verbose_name="Texto")
    created = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Fecha de última modificación", auto_now=True)

    class Meta:
        verbose_name = "sección"
        verbose_name_plural = "secciones"
        ordering = ["-created"]
    
    def __str__(self) -> str:
        return self.text
    
class Question(models.Model):
    question_order = models.CharField(verbose_name="Orden", max_length=10)
    number = models.IntegerField(verbose_name="Número")
    content = models.CharField(verbose_name="Contenido", max_length=500)
    type = models.IntegerField(verbose_name="Tipo")
    section = models.ForeignKey(Section, verbose_name="Secciones", on_delete=models.SET_DEFAULT, default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "pregunta"
        verbose_name_plural = "preguntas"
        ordering = ['-updated', 'question_order']

    def __str__(self):
        return self.content

class Item(models.Model):
    item_order = models.IntegerField(verbose_name="Orden")
    text = models.CharField(max_length=500, verbose_name="Texto")
    question = models.ForeignKey(Question, verbose_name="Preguntas", on_delete=models.SET_DEFAULT, default=0)
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
    item = models.ForeignKey(Item, verbose_name="Opciones", on_delete=models.SET_DEFAULT, default=0)
    created = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Fecha de última modificación", auto_now=True)

    class Meta:
        verbose_name = "opción"
        verbose_name_plural = "opciones"
        ordering = ["option_order"]
    
    def __str__(self) -> str:
        return self.text
    
# from django.db import models
# from django.utils.timezone import now
# from django.contrib.auth.models import User

# # Create your models here.
# class Category(models.Model):
#     name = models.CharField(max_length=100, verbose_name="Nombre")
#     subtitle = models.CharField(max_length=200, verbose_name="Subtítulo")
#     created = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
#     updated = models.DateTimeField(verbose_name="Fecha de última modificación", auto_now=True)

#     class Meta:
#         verbose_name = "categoría"
#         verbose_name_plural = "categorías"
#         ordering = ["-created"]
    
#     def __str__(self) -> str:
#         return self.name
    
# class Post(models.Model):
#     title = models.CharField(max_length=200, verbose_name="Título")
#     content = models.TextField(verbose_name="Contenido")
#     published = models.DateTimeField(verbose_name="Fecha de publicación", default=now)
#     image = models.ImageField(verbose_name="Imagen", upload_to="blog", null=True, blank=True)
#     author = models.ForeignKey(User, verbose_name="Autor", on_delete=models.CASCADE)
#     categories = models.ManyToManyField(Category, verbose_name="Categorías", related_name="get_posts")
#     created = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
#     updated = models.DateTimeField(verbose_name="Fecha de última modificación", auto_now=True)

#     class Meta:
#         verbose_name = "entrada"
#         verbose_name_plural = "entradas"
#         ordering = ["created"]
    
#     def __str__(self) -> str:
#         return self.title