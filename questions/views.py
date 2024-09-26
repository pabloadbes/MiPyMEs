from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Question, Item, Option
from surveys.models import Survey, Response, Variable, Variable_List
from companies.models import Company, District, City
from team.models import Supervisor, Surveyor
from questions.processors import ctx_dict

# Create your views here.
# class QuestionsListView(ListView): DEFINIR SI ES NECESARIA
#     model = Question

@method_decorator(login_required, name='dispatch')
class QuestionDetail(TemplateView):
    template_name = 'questions/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = Question.objects.get(id = context['pk'])
        context["survey_data"] = Survey.objects.get(id = context['survey'])
        ctx = ctx_dict(self.request)
        if "init_1" in ctx['template_type']:
            context["supervisor"] = Company.objects.get(id = context["survey_data"].company.id).supervisor
            context["surveyors"] = Surveyor.objects.all()
        elif "init_3" in ctx['template_type']:
            company = Company.objects.get(id = context["survey_data"].company.id)
            city = company.city
            context["city_registered"] = city
            context["districts"] = District.objects.all()
            context["cities"] = City.objects.all().exclude(id = city.id)

        return context

    def post(self, request, *args, **kwargs):
        user_id = self.request.user
        context = self.get_context_data(**kwargs)
        survey_id = context['survey']
        survey = Survey.objects.get(pk = survey_id)
        question = context['question']

        # if survey.is_survey_complete():
        #     survey.set_survey_state(2)
        # survey.set_next_question(survey.calculate_next_question())
        # if question.number > 0:
        #     survey.set_progress(100 * question.number / survey.get_number_of_questions())
        # else:
        #     survey.set_progress(0)
        # survey.set_updated_by(user_id)

        ctx = ctx_dict(request)
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        data.pop('question_metadata',0)

        # print("********************************************************")
        # print("EN EL POST")
        # print("CONTEXT")
        # print(context)
        # print("********************************************************")
        # print("CTX")
        # print(ctx)
        print("********************************************************")
        print("DATA")
        print(data)
        # print("DATA ELIMINANDO EL PRIMERO")
        data.pop('question_type',0)
        # print(data)
        # print("********************************************************")
        # for item in ctx['items']:
        #     print(item)
        #     for option in item[1]:
        #         print(option[0])
        #         if option[0].children_id:
        #             print(option[0].children_id)
        #             children_item = Item.objects.get(id = option[0].children_id)
        #             print(children_item)
        #             children_options = Option.objects.filter(item_id = children_item.id)

        #             for children_option in children_options:
        #                 print(children_option)
        try:
            with transaction.atomic():
                if "text" in ctx['template_type'] or "number" in ctx['template_type'] or "scale" in ctx['template_type'] or "year" in ctx['template_type'] or "total" in ctx['template_type']:
                    for d in data:
                        response = Response.objects.create(value = data[d], option_id = d, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                        response.save()
                        if Variable_List.objects.all().filter(option_id = d).exists():
                            vble = Variable_List.objects.get(option_id = d)
                            variable = Variable.objects.create(value = data[d], survey_id = survey.id, variable_list_id = vble.id, created_by = user_id, updated_by = user_id)   
                            variable.save()
                
                elif "select_one" in ctx['template_type']:
                    for item in ctx['items']:
                        for option in item[1]:
                            if Variable_List.objects.all().filter(option_id = option[0].id).exists():
                                vble = Variable_List.objects.get(option_id = option[0].id)
                            if option[0].text == data[str(item[0].id)]:
                                response = Response.objects.create(value = "true", option_id = option[0].id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                                variable = Variable.objects.create(value = option[0].code, survey_id = survey.id, variable_list_id = vble.id, created_by = user_id, updated_by = user_id)   
                                variable.save()
                            else: 
                                response = Response.objects.create(value = "false", option_id = option[0].id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                            if option[0].children_id:
                                children_item = Item.objects.get(id = option[0].children_id)
                                children_option = Option.objects.get(item_id = children_item.id)
                                children_vble = Variable_List.objects.get(option_id = children_option.id)
                                if str(children_option.id) in data:
                                    children_response = Response.objects.create(value = data[str(children_option.id)], option_id = children_option.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                                    children_response.save()
                                    children_exists = Variable.objects.all().filter(survey_id = survey.id,variable_list_id = children_vble.id).exists()
                                    if not children_exists:
                                        children_variable = Variable.objects.create(value = data[str(children_option.id)], survey_id = survey.id, variable_list_id = children_vble.id, created_by = user_id, updated_by = user_id)   
                                        children_variable.save()
                            response.save()

                elif "double_select" in ctx['template_type'] or "double_check_txt" in ctx['template_type']:
                    for item in ctx['items']:
                        for option in item[1]:
                            if Variable_List.objects.all().filter(option_id = option[0].id).exists():
                                vble = Variable_List.objects.get(option_id = option[0].id)
                            if option[0].text == data[str(item[0].id)]:
                                response = Response.objects.create(value = "true", option_id = option[0].id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                                variable = Variable.objects.create(value = option[0].code, survey_id = survey.id, variable_list_id = vble.id, created_by = user_id, updated_by = user_id)   
                                variable.save()
                            else: 
                                response = Response.objects.create(value = "false", option_id = option[0].id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                            if option[0].children_id:
                                children_item = Item.objects.get(id = option[0].children_id)
                                children_options = Option.objects.all().filter(item_id = children_item.id)
                                if len(children_options) == 1:
                                    children_option = children_options.first()
                                    if data.get(str(children_option.id), False):
                                        children_response = Response.objects.create(value = data[str(children_option.id)], option_id = children_option.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                                        response.save()
                                        if Variable_List.objects.all().filter(option_id = children_option.id).exists():
                                            vble = Variable_List.objects.get(option_id = children_option.id)
                                            variable = Variable.objects.create(value = data[str(children_option.id)], survey_id = survey.id, variable_list_id = vble.id, created_by = user_id, updated_by = user_id)   
                                            variable.save()
                                else:
                                    for children_option in children_options:
                                        if Variable_List.objects.all().filter(option_id = children_option.id).exists():
                                            children_vble = Variable_List.objects.get(option_id = children_option.id)
                                        if data.get(str(children_item.id), False) and children_option.text == data[str(children_item.id)]:
                                            children_response = Response.objects.create(value = True, option_id = children_option.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                                            children_variable = Variable.objects.create(value = str(children_option.code), survey_id = survey.id, variable_list_id = children_vble.id, created_by = user_id, updated_by = user_id)   
                                            children_response.save()
                                            children_variable.save()
                                        else:
                                            children_response = Response.objects.create(value = False, option_id = children_option.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                                        children_response.save()
                            response.save()

                elif "select_many" in ctx['template_type']: #falta poner a prueba este caso
                    selected_options = data.keys()
                    for item in ctx['items']:
                        for option in item[1]:
                            if Variable_List.objects.all().filter(option_id = option[0].id).exists():
                                vble = Variable_List.objects.get(option_id = option[0].id)
                            if str(option[0].id) in selected_options:
                                response = Response.objects.create(value = "true", option_id = option[0].id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                                variable = Variable.objects.create(value = option[0].id, survey_id = survey.id, variable_list_id = vble.id, created_by = user_id, updated_by = user_id)   
                                variable.save()                                
                            else: 
                                response = Response.objects.create(value = "false", option_id = option[0].id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                            response.save()

                if "txt_sel" in ctx['template_type']:
                    items = ctx['items']
                    [txt_item, sel_item] = items

                    txt_option_id = txt_item[1][0][0].id
                    txt_response = Response.objects.create(value = data[str(txt_option_id)], option_id = txt_option_id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    txt_response.save()
                    if Variable_List.objects.all().filter(option_id = txt_option_id).exists():
                        txt_vble = Variable_List.objects.get(option_id = txt_option_id)
                        txt_variable = Variable.objects.create(value = data[str(txt_option_id)], survey_id = survey.id, variable_list_id = txt_vble.id, created_by = user_id, updated_by = user_id)   
                        txt_variable.save()

                    for sel_option in sel_item[1]:
                        if Variable_List.objects.all().filter(option_id = sel_option[0].id).exists():
                            sel_vble = Variable_List.objects.get(option_id = sel_option[0].id)
                        if sel_option[0].text == data[str(sel_item[0].id)]:
                            sel_response = Response.objects.create(value = "true", option_id = sel_option[0].id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                            sel_variable = Variable.objects.create(value = sel_option[0].code, survey_id = survey.id, variable_list_id = sel_vble.id, created_by = user_id, updated_by = user_id)   
                            sel_variable.save()
                        else: 
                            sel_response = Response.objects.create(value = "false", option_id = sel_option[0].id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                        sel_response.save()

                elif "init_1" in ctx['template_type']:
                    item = ctx['items'][0]
                    option_encuestador = item[1][1][0]
                    vble_tipo_cuest = Variable_List.objects.get(option_id = item[1][0][0].id)
                    vble_encuestador = Variable_List.objects.get(option_id = item[1][1][0].id)
                    vble_supervisor = Variable_List.objects.get(option_id = item[1][2][0].id)
                    response_encuestador = Response.objects.create(value = data['surveyor'], option_id = option_encuestador.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    variable_tipo_cuest = Variable.objects.create(value = survey.survey_type.id, survey_id = survey.id, variable_list_id = vble_tipo_cuest.id, created_by = user_id, updated_by = user_id)
                    variable_encuestador = Variable.objects.create(value = data['surveyor'], survey_id = survey.id, variable_list_id = vble_encuestador.id, created_by = user_id, updated_by = user_id)
                    variable_supervisor = Variable.objects.create(value = context['supervisor'].SUP_CODE, survey_id = survey.id, variable_list_id = vble_supervisor.id, created_by = user_id, updated_by = user_id)

                    response_encuestador.save()
                    variable_tipo_cuest.save()
                    variable_encuestador.save()
                    variable_supervisor.save()

                elif "init_2" in ctx['template_type']:
                    item_entrevista = ctx['items'][0]
                    item_fecha = ctx['items'][1]
                    option_entrevista = item_entrevista[1][0][0]
                    option_fecha = item_fecha[1][0][0]
                    vble_entrevista = Variable_List.objects.get(option_id = item_entrevista[1][0][0].id)
                    vble_fecha = Variable_List.objects.get(option_id = item_fecha[1][0][0].id)
                    response_entrevista = Response.objects.create(value = data['entrevista'], option_id = option_entrevista.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    response_fecha = Response.objects.create(value = data['fecha'], option_id = option_fecha.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    variable_entrevista = Variable.objects.create(value = data['entrevista'], survey_id = survey.id, variable_list_id = vble_entrevista.id, created_by = user_id, updated_by = user_id)
                    variable_fecha = Variable.objects.create(value = data['fecha'], survey_id = survey.id, variable_list_id = vble_fecha.id, created_by = user_id, updated_by = user_id)

                    response_entrevista.save()
                    response_fecha.save()
                    variable_entrevista.save()
                    variable_fecha.save()

                elif "init_3" in ctx['template_type']:
                    item = ctx['items'][0]
                    option_provincia = item[1][0][0]
                    option_departamento = item[1][1][0]
                    option_localidad = item[1][2][0]
                    option_cod_emp = item[1][3][0]
                    vble_provincia = Variable_List.objects.get(option_id = item[1][0][0].id)
                    vble_departamento = Variable_List.objects.get(option_id = item[1][1][0].id)
                    vble_localidad = Variable_List.objects.get(option_id = item[1][2][0].id)
                    vble_cod_emp = Variable_List.objects.get(option_id = item[1][3][0].id)

                    response_provincia = Response.objects.create(value = '94', option_id = option_provincia.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    response_departamento = Response.objects.create(value = data['district'], option_id = option_departamento.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    response_localidad = Response.objects.create(value = data['city'], option_id = option_localidad.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    response_cod_emp = Response.objects.create(value = data['due_id'], option_id = option_cod_emp.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)

                    variable_provincia = Variable.objects.create(value = '94', variable_list_id = vble_provincia.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    variable_departamento = Variable.objects.create(value = data['district'], variable_list_id = vble_departamento.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    variable_localidad = Variable.objects.create(value = data['city'], variable_list_id = vble_localidad.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    variable_cod_emp = Variable.objects.create(value = data['due_id'], variable_list_id = vble_cod_emp.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)

                    response_provincia.save()
                    response_departamento.save()
                    response_localidad.save()
                    response_cod_emp.save()
                    
                    variable_provincia.save()
                    variable_departamento.save()
                    variable_localidad.save()
                    variable_cod_emp.save()

                elif "init_4" in ctx['template_type']:
                    item = ctx['items'][0]
                    option_cuit = item[1][0][0]
                    option_name = item[1][1][0]
                    option_address_street = item[1][2][0]
                    option_address_number = item[1][3][0]
                    option_zip_code = item[1][4][0]
                    option_phone = item[1][5][0]
                    option_email = item[1][6][0]
                    option_web_page = item[1][7][0]
                    vble_cuit = Variable_List.objects.get(option_id = item[1][0][0].id)
                    vble_name = Variable_List.objects.get(option_id = item[1][1][0].id)
                    vble_address_street = Variable_List.objects.get(option_id = item[1][2][0].id)
                    vble_address_number = Variable_List.objects.get(option_id = item[1][3][0].id)
                    vble_zip_code = Variable_List.objects.get(option_id = item[1][4][0].id)
                    vble_phone = Variable_List.objects.get(option_id = item[1][5][0].id)
                    vble_email = Variable_List.objects.get(option_id = item[1][6][0].id)
                    vble_web_page = Variable_List.objects.get(option_id = item[1][7][0].id)

                    response_cuit = Response.objects.create(value = context["survey_data"].company.cuit, option_id = option_cuit.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    response_name = Response.objects.create(value = data['name'], option_id = option_name.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    response_address_street = Response.objects.create(value = data['street'], option_id = option_address_street.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    response_address_number = Response.objects.create(value = data['number'], option_id = option_address_number.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    response_zip_code = Response.objects.create(value = data['zip_code'], option_id = option_zip_code.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    response_phone = Response.objects.create(value = data['phone'], option_id = option_phone.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    response_email = Response.objects.create(value = data['email'], option_id = option_email.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    response_web_page = Response.objects.create(value = data['web_page'], option_id = option_web_page.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)

                    variable_cuit = Variable.objects.create(value = context["survey_data"].company.cuit, variable_list_id = vble_cuit.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    variable_name = Variable.objects.create(value = data['name'], variable_list_id = vble_name.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    variable_address_street = Variable.objects.create(value = data['street'], variable_list_id = vble_address_street.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    variable_address_number = Variable.objects.create(value = data['number'], variable_list_id = vble_address_number.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    variable_zip_code = Variable.objects.create(value = data['zip_code'], variable_list_id = vble_zip_code.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    variable_phone = Variable.objects.create(value = data['phone'], variable_list_id = vble_phone.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    variable_email = Variable.objects.create(value = data['email'], variable_list_id = vble_email.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)
                    variable_web_page = Variable.objects.create(value = data['web_page'], variable_list_id = vble_web_page.id, survey_id = survey.id, created_by = user_id, updated_by = user_id)

                    response_cuit.save()
                    response_name.save()
                    response_address_street.save()
                    response_address_number.save()
                    response_zip_code.save()
                    response_phone.save()
                    response_email.save()
                    response_web_page.save()
                    
                    variable_cuit.save()
                    variable_name.save()
                    variable_address_street.save()
                    variable_address_number.save()
                    variable_zip_code.save()
                    variable_phone.save()
                    variable_email.save()
                    variable_web_page.save()



            if survey.is_survey_complete():
                survey.set_survey_state(2)
            survey.set_next_question(survey.calculate_next_question())
            if question.number > 0:
                survey.set_progress(100 * question.number / survey.get_number_of_questions())
            else:
                survey.set_progress(0)
            survey.set_updated_by(user_id)
            survey.save()

        except Exception as e:
            print(f"Error: No se guardó la respuesta {e}")
            return HttpResponseRedirect(reverse_lazy("surveys:surveys"))
        # print("CANTIDAD DE PREGUNTAS")
        # print(survey.get_number_of_questions())
        # print("NÚMERO DE PREGUNTA")
        # print(question.number)
        if question.number == survey.get_number_of_questions():
            return HttpResponseRedirect(reverse_lazy("surveys:end", args=[survey.id]))
        return HttpResponseRedirect(reverse_lazy("questions:question_detail", kwargs={'pk':survey.next_question, 'survey':survey.id}))


# question types
# 1:text
# 2:number
# 3:scale
# 4:select
# 5:multiple select
