from typing import List
from django.db import models
from django.contrib.auth.models import User
from companies.models import Company
from questions.models import Option, Survey_Type, Question, Section

class Survey_State(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=50)
    description = models.CharField(verbose_name="Descripción", max_length=500)
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="survey_state_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="survey_state_updated_by_user")

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
    progress = models.IntegerField(verbose_name="Progreso", default=0)
    next_question = models.IntegerField(verbose_name="Pregunta siguiente", default=0)
    number_of_questions = models.IntegerField(verbose_name="Cantidad de preguntas", default=0)
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="survey_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="survey_updated_by_user")

    class Meta:
        verbose_name = "encuesta"
        verbose_name_plural = "encuestas"
        ordering = ['-updated_at', 'company']

    def __str__(self):
        return self.company.name

    def save(self, *args, **kwargs) -> None:
        if(Survey.objects.all().filter(company_id=self.company.id)):    #Si la encuesta ya existe
            if(not self.id):                                            #Si no tiene id, estamos creando encuesta que ya existe, no hacemos nada (return vacío)
                return
        return super().save(*args, **kwargs)
    
    def get_survey_type(self) -> str:
        return str(self.survey_type)
    
    def get_survey_state(self) -> str:
        return str(self.survey_state)
    
    def set_survey_state(self, survey_state_id:int) -> None:
        self.survey_state_id = survey_state_id

    def get_progress(self) -> int:
        return self.progress
    
    def set_progress(self, progress:int) -> None:
        self.progress = progress

    def get_created_by(self) -> int:
        return self.created_by
    
    def set_created_by(self, user_id:int) -> None:
        self.created_by = user_id

    def get_updated_by(self) -> int:
        return self.updated_by
    
    def set_updated_by(self, user_id:int) -> None:
        self.updated_by = user_id

    def get_next_question(self) -> int:
        try:
            return Question.objects.get(id = self.next_question).id
        except:
            return 1

    def set_next_question(self, next_question_id:int) -> None:
        self.next_question = next_question_id        

    def get_number_of_questions(self) -> int:
        return self.number_of_questions
    
    def set_number_of_questions(self, number_of_questions:int) -> None:
        self.number_of_questions = number_of_questions

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
        questions.sort(key = lambda question:question.number)
        return questions[0].id
    
    def get_last_question(self) -> int:
        questions = self.get_questions()
        questions.sort(key = lambda question:question.number, reverse=True)
        return questions[0].id
    
    def is_survey_complete(self) -> bool:
        return self.get_next_question() == self.get_number_of_questions() + self.get_first_question() - 1
    
    def calculate_next_question(self) -> int:
        #Al iniciar la encuesta debe indicar la primera pregunta
        if self.get_survey_state() == "created":
            if self.get_next_question() == 0:
                return self.get_first_question()
        #Debe detectar si la encuesta se completó
            if self.is_survey_complete():
                return self.get_last_question()
        #Durante el llenado debe indicar la pregunta siguiente
            self.set_next_question(self.get_next_question() + 1)
        #Evaluar filtros
        
        return self.next_question

class Response(models.Model):
    value = models.CharField(verbose_name="Valor", max_length=500)
    survey = models.ForeignKey(Survey, verbose_name="Empresa", on_delete=models.SET_DEFAULT, default=0)
    option = models.ForeignKey(Option, verbose_name="Opción", on_delete=models.SET_DEFAULT, default=0)
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="response_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="response_updated_by_user")

    class Meta:
        verbose_name = "respuesta"
        verbose_name_plural = "respuestas"
        ordering = ['survey', '-updated_at']

    def __str__(self):
        return self.survey.company.name
    
class Variable_Type(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=50)
    description = models.CharField(verbose_name="Descripción", max_length=500)
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="variable_type_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="variable_type_updated_by_user")

    class Meta:
        verbose_name = "Tipo de variable estadística de interés"
        verbose_name_plural = "Tipos de variable estadística de interés"
        ordering = ['name']

    def __str__(self):
        return self.name

class Variable_List(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=500)
    variable_type = models.ForeignKey(Variable_Type, verbose_name="Tipo de variable", on_delete=models.SET_DEFAULT, default=0)
    option = models.ForeignKey(Option, verbose_name="Opción", on_delete=models.SET_DEFAULT, default=0)
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="variable_list_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="variable_list_updated_by_user")

    class Meta:
        verbose_name = "Tabla de variables estadísticas de interés"
        verbose_name_plural = "Tabla de variables estadísticas de interés"
        ordering = ['name', '-updated_at']

    def __str__(self):
        return self.name
    
class Variable(models.Model):
    value = models.CharField(verbose_name="Valor", max_length=500)
    survey = models.ForeignKey(Survey, verbose_name="Encuesta", on_delete=models.SET_DEFAULT, default=0)
    variable_list = models.ForeignKey(Variable_List, verbose_name="Listado de variables", on_delete=models.SET_DEFAULT, default=0)
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="variables_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="variable_updated_by_user")

    class Meta:
        verbose_name = "Variable estadística de interés"
        verbose_name_plural = "Variables estadísticas de interés"
        ordering = ['survey', '-updated_at']

    def __str__(self):
        return self.survey