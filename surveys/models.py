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
        section_ids = list(Section.objects.all().filter(survey_type = self.survey_type).values_list('id', flat=True).order_by('id'))
        questions = []
        for section_id in section_ids:
            questions.extend(list(Question.objects.all().filter(section_id = section_id).order_by('id')))
        return questions
    
    def calculate_number_of_questions(self) -> int:
        return len(self.get_questions()) - 4 # Las primeras cuatro no se cuentan
    
    def get_first_question(self) -> int:
        questions = self.get_questions()
        questions.sort(key = lambda question:question.number)
        return questions[0].id
    
    def get_last_question(self) -> int:
        questions = self.get_questions()
        questions.sort(key = lambda question:question.number, reverse=True)
        return questions[0].id
    
    def is_survey_complete(self) -> bool:
        return self.get_next_question() == self.get_number_of_questions() + self.get_first_question() + 3
    
    def calculate_next_question(self) -> int:
        #Al iniciar la encuesta debe indicar la primera pregunta
        if self.get_survey_state() == "created":
        #Debe detectar si la encuesta se completó
            if self.is_survey_complete():
                return self.get_last_question()
        #Durante el llenado debe indicar la pregunta siguiente o el pase
            answering_question = Survey_Questions.objects.get(survey_id = self.id, survey_question_state_id = 4)
            answering_question.survey_question_state_id = 2
            answering_question.save()
            if Filter.objects.all().filter(question_id = answering_question.question.id).exists():
                filters = Filter.objects.all().filter(question_id = answering_question.question.id)
                for filter in filters:
                    filter_variables = filter.variables.all()
                    if filter.evaluation(self):
                        if filter.filter_type_id == 1:
                            for i in range(answering_question.question.id+1,filter.dest):
                                passed_question = Survey_Questions.objects.get(survey_id = self.id, question_id = i)
                                passed_question.survey_question_state_id = 3
                                passed_question.save()
                        elif filter.filter_type_id in (2, 3, 4, 5):
                            passed_question = Survey_Questions.objects.get(survey_id = self.id, question_id = filter.dest)
                            passed_question.survey_question_state_id = 3
                            passed_question.save()

            next_question = Survey_Questions.objects.all().filter(survey_id = self.id).filter(survey_question_state_id = 1).first()
            self.set_next_question(next_question.question.id)
            self.save()
            next_question.survey_question_state_id = 4
            next_question.save()

        return self.next_question

class Survey_Question_State(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=50)
    description = models.CharField(verbose_name="Descripción", max_length=500)
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="survey_question_state_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="survey_question_state_updated_by_user")

    class Meta:
        verbose_name = "Estado de preguntas de la encuesta"
        verbose_name_plural = "Estados de preguntas de la encuesta"
        ordering = ['name']

    def __str__(self):
        return self.name

class Survey_Questions(models.Model):
    survey = models.ForeignKey(Survey, verbose_name="Empresa", on_delete=models.SET_DEFAULT, default=0)
    question = models.ForeignKey(Question, verbose_name="Pregunta", on_delete=models.SET_DEFAULT, default=0)
    survey_question_state = models.ForeignKey(Survey_Question_State, verbose_name="Estado de la pregunta", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="pregunta_pendiente_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="pregunta_pendiente_by_user")

    class Meta:
        verbose_name = "preguntas restantes de encuesta"
        verbose_name_plural = "preguntas restantes de encuesta"
        ordering = ['survey', 'question']

    def __str__(self):
        return self.survey.company.name + " - " + str(self.question.number) + ". " + self.question.text
    
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
        return self.variable_list.name + " " + self.value
    
class Condition_Type(models.Model):
    symbol = models.CharField(max_length=2 ,verbose_name="símbolo")
    description = models.CharField(max_length=500, verbose_name="Descripción")
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="condition_type_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="condition_type_updated_by_user")

    class Meta:
        verbose_name = "Tipo de condición"
        verbose_name_plural = "Tipos de condición"
        ordering = ["description"]
        
    def __str__(self) -> str:
        return self.description
    
class Filter_Type(models.Model):
    name = models.CharField(verbose_name="nombre")
    description = models.CharField(max_length=500, verbose_name="Descripción")
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="filter_type_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="filter_type_updated_by_user")

    class Meta:
        verbose_name = "Tipo de filtro"
        verbose_name_plural = "Tipos de filtro"
        ordering = ["name"]
        
    def __str__(self) -> str:
        return self.name

class Filter(models.Model):
    question = models.ForeignKey(Question, verbose_name="pregunta", on_delete=models.DO_NOTHING)
    variables = models.ManyToManyField(Variable_List, verbose_name="Variables")
    filter_type = models.ForeignKey(Filter_Type, verbose_name="Tipo de filtro", on_delete=models.DO_NOTHING)
    condition_type = models.ForeignKey(Condition_Type, verbose_name="Condición", on_delete=models.DO_NOTHING)
    value = models.IntegerField(verbose_name="Valor")
    dest = models.IntegerField(verbose_name="Destino")
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="filter_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="filter_updated_by_user")

    class Meta:
        verbose_name = "Filtro"
        verbose_name_plural = "Filtros"
        ordering = ["question"]
        
    def __str__(self) -> str:
        return self.filter_type.name + self.condition_type.symbol
    
    def evaluation(self, survey: Survey) -> bool:
        if self.filter_type_id in (1, 2):
            variable_list_id = self.variables.all().first()
            variable = Variable.objects.get(survey_id = survey.id, variable_list_id = variable_list_id)
            if self.condition_type_id == 1:
                if self.value == int(variable.value):
                    return True
                else:
                    return False
            elif self.condition_type_id == 2:
                if self.value > int(variable.value):
                    return True
                else:
                    return False
            elif self.condition_type_id == 3:
                if self.value < int(variable.value):
                    return True
                else:
                    return False
            elif self.condition_type_id == 4:
                if self.value != int(variable.value):
                    return True
                else:
                    return False
        else:
            filter_variable_list = self.variables.all().values_list('id', flat=True)
            variables = Variable.objects.all().filter(survey_id = survey.id).filter(variable_list_id__in = filter_variable_list)
            if self.filter_type_id == 3:
                if self.condition_type_id == 4:
                    resultado = True
                    for variable in variables:
                        resultado = resultado and int(variable.value) != self.value
                    return resultado
            elif self.filter_type_id == 4:
                if self.condition_type_id == 3:
                    resultado = False
                    for variable in variables:
                        resultado = resultado or int(variable.value) > self.value
                    return resultado
                elif self.condition_type_id == 4:
                    resultado = False
                    for variable in variables:
                        resultado = resultado or int(variable.value) != self.value
                    return resultado
            return False
        

class Validationjs(models.Model):
    name = models.CharField(max_length=500, verbose_name="Nombre")
    question = models.ForeignKey(Question, verbose_name="pregunta", on_delete=models.DO_NOTHING)
    condition_type = models.ForeignKey(Condition_Type, verbose_name="Condición", on_delete=models.DO_NOTHING)
    value = models.IntegerField(verbose_name="Valor")
    created_at = models.DateTimeField(verbose_name="Creado el", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificado el", auto_now=True)
    created_by = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.CASCADE, related_name="validationjs_created_by_user")
    updated_by = models.ForeignKey(User, verbose_name="Modificado por", on_delete=models.CASCADE, related_name="validationjs_updated_by_user")

    class Meta:
        verbose_name = "Validación JS"
        verbose_name_plural = "Validaciones JS"
        ordering = ["name"]
    
    def __str__(self) -> str:
        return self.name