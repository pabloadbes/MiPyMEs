from .models import Question, Item, Option, Note
from companies.models import Company
from surveys.models import Survey, Validationjs
import json

def ctx_dict(request):
   ctx = {}
   
   page = page_request(request)
   if page == "home":
      return ctx
   elif page == "questions":
      ctx = ctx_questions(request)
   # elif page == "surveys":
   #    ctx = ctx_surveys(request)
   return ctx

# question types
# 1:text
# 2:number
# 3:scale
# 4:select
# 5:multiple select

def page_request(request):
   aux = request.__str__().split("/")
   if (aux[1]=="'>"):
      return "home"
   else:
      return aux[1]
   
def ctx_questions(request):
   aux = request.__str__().split("/")
   question_id = aux[2]
   question = Question.objects.get(id = question_id)
   survey_id = aux[3]
   company_id = Survey.objects.get(id = survey_id).company_id
   company = Company.objects.get(id = company_id)
   template_type = "./question_detail_type_" + question.question_type.__str__() + ".html"
   question_metadata = dict(question_type = question.question_type.__str__())
   items = []
   its = Item.objects.all().filter(question_id = question_id)
   for item in its:
      hide_item = False
      opts = Option.objects.all().filter(item_id = item)
      options = []
      if question.question_type.__str__() == "double_select":
         for option in opts:
            if option.children:
               question_metadata[option.id] = []
               child_items = []
               child_its = Item.objects.all().filter(id = option.children.id)
               for child_item in child_its:
                  child_options = []
                  child_opts = Option.objects.all().filter(item_id = child_item.id)
                  for child_option in child_opts:
                     child_options.append(child_option)
                     question_metadata[option.id].append(child_option.id)
                  child_items.append([child_item, child_options])
               options.append([option, child_items])
            else:
               options.append([option])
         items.append([item, options])
            
      else:
         for option in opts:
            nts = Note.objects.all().filter(option_id = option.id)
            notes = []
            for note in nts:
               notes.append(note.text)
            if option.children:
               child_items = []
               child_its = Item.objects.all().filter(id = option.children.id)
               for child_item in child_its:
                  child_options = []
                  child_opts = Option.objects.all().filter(item_id = child_item.id)
                  for child_option in child_opts:
                     child_options.append(child_option)
                     if child_option.id in question_metadata.values():
                        hide_item = True
                     question_metadata[option.id] = child_option.id
                  child_items.append([child_item, child_options, hide_item])
               options.append([option, notes, child_items])
            else:
               options.append([option, notes])   
         items.append([item, options])
   
   question_metadata['validation'] = []
   if Validationjs.objects.all().filter(question_id = question_id).exists():
      validations = Validationjs.objects.all().filter(question_id = question_id)
      for val in validations:
         question_metadata['validation'].append([val.name, val.value, val.condition_type.symbol])
   json_question_metadata = json.dumps(question_metadata)
   ctx = {}
   ctx['company'] = company
   ctx['items'] = items
   ctx['template_type'] = template_type
   ctx['question_metadata'] = json_question_metadata
   return ctx