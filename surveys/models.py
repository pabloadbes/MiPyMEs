import unicodedata
from typing import Iterable, List
from django.db import models
from companies.models import Company
from questions.models import Option, Survey_Type, Question, Section

class Survey_State(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=50)
    description = models.CharField(verbose_name="Descripción", max_length=500)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "Estado de la encuesta"
        verbose_name_plural = "Estados de la encuesta"
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Survey(models.Model):
    company = models.ForeignKey(Company, verbose_name="Empresa", on_delete=models.SET_DEFAULT, default=0)
    survey_type = models.ForeignKey(Survey_Type, verbose_name="Tipo de Encuesta", on_delete=models.SET_DEFAULT, default=1)
    survey_state = models.ForeignKey(Survey_State, verbose_name="Estado de la Encuesta", on_delete=models.SET_DEFAULT, default=1)
    progress = models.IntegerField(verbose_name="Progreso", default=1)
    next_question = models.IntegerField(verbose_name="Pregunta siguiente", default=1)
    number_of_questions = models.IntegerField(verbose_name="Cantidad de preguntas", default=1)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "encuesta"
        verbose_name_plural = "encuestas"
        ordering = ['-updated', 'company']

    def __str__(self):
        return self.company.name

    def save(self, *args, **kwargs) -> None:
        print("DENTRO DEL SAVE()")
        print("ESTE ES EL SELF QUE RECIBO EN EL SAVE() DE SURVEY")
        print(self)
        if(Survey.objects.all().filter(company_id=self.company.id)):    #Si la encuesta ya existe
            if(not self.id):                                            #Si no tiene id, estamos creando encuesta que ya existe, no hacemos nada (return vacío)
                print("NO GUARDAMOS NADA PAPÁ")                                                        #Si tiene id, estamos en otra pantalla que no es creación, salimos del if y retornamos el save por defecto, sí guardamos cambios
                return
        print("SI GUARDAMOS")
        return super().save(*args, **kwargs)

    def get_questions(self) -> List[Question]:
        section_ids = list(Section.objects.all().filter(survey_type = self.survey_type).values_list('id', flat=True))
        questions = []
        for section_id in section_ids:
            questions.extend(list(Question.objects.all().filter(section_id = section_id).order_by('id')))
        return questions
    
    def calculate_number_of_questions(self) -> int:
        return len(self.get_questions())
    
    def get_first_question(self) -> int:
        questions = self.get_questions()
        for question in questions:
            print(question)
        questions.sort(key = lambda question:question.number)
        return questions[0].id
    
    def get_last_question(self) -> int:
        questions = self.get_questions()
        questions.sort(key = lambda question:question.number, reverse=True)
        return questions[0].id
    
    def get_next_question(self) -> int:
        return Question.objects.get(id = self.next_question).values('id')
    
    def calculate_next_question(self) -> int:
        #Al iniciar la encuesta debe indicar la primera pregunta
        print("ESTADO DE LA ENCUESTA")
        if str(self.survey_state) == "created":
            print("NO COMPLETA")
            if self.next_question == 1:
                print("NO INICIADA")
                return self.get_first_question()
        #Debe detectar si la encuesta se completó
            if self.next_question == self.get_number_of_questions():
                self.survey_state = 2
                return self.get_last_question()
        #Durante el llenado debe indicar la pregunta siguiente
            self.next_question = self.next_question + 1
        #Evaluar filtros
        
        return self.next_question

    # def __get_first_question__(self) -> List[Question]:
    #     section_ids = list(Section.objects.all().filter(survey_type = self.survey_type).values_list('id', flat=True))
    #     question_ids = []
    #     for section_id in section_ids:
    #         question_ids.extend(list(Question.objects.all().filter(section_id = section_id).order_by('id').values_list('id', flat=True)))

    #         survey_questions = len(question_ids)
    #         survey.number_of_questions = survey_questions
    #         survey.next_question = question_ids[0]
    #         survey.progress = 0
    #         survey.save()

    #     return Question.objects.all()
    
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