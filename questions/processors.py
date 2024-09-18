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
   print("**************************************************")
   print("PROCESORS")
   print("**************************************************")
   aux = request.__str__().split("/")
   question_id = aux[2]
   question = Question.objects.get(id = question_id)
   survey_id = aux[3]
   company_id = Survey.objects.get(id = survey_id).company_id
   company = Company.objects.get(id = company_id)
   template_type = "./question_detail_type_" + question.question_type.__str__() + ".html"
   print(template_type)
   question_metadata = dict(question_type = question.question_type.__str__())
   items = []
   its = Item.objects.all().filter(question_id = question_id)
   for item in its:
      hide_item = False
      opts = Option.objects.all().filter(item_id = item)
      options = []
      if question.question_type.__str__() == "double_select" or question.question_type.__str__() == "double_check_txt":
         print("ES DOUBLE SELECT")
         for option in opts:
            print("OPTION")
            print(option)
            print("INICIALIZO METADATA para esta option")
            
            if option.children:
               print("HAY HIJO")
               question_metadata[option.id] = []
               child_items = []
               child_its = Item.objects.all().filter(id = option.children.id)
               for child_item in child_its:
                  child_options = []
                  child_opts = Option.objects.all().filter(item_id = child_item.id)
                  for child_option in child_opts:
                     child_options.append(child_option)
                     #if child_option.id in question_metadata.values():
                     question_metadata[option.id].append(child_option.id)
                     print("question_metadata del double select")
                     print(question_metadata[option.id])
                     # question_metadata[option.id] = child_option.id
                     # print("METADATA")
                     # print(question_metadata)
                  child_items.append([child_item, child_options])
               options.append([option, child_items])
            else:
               print("NO HAY HIJO")
               options.append([option])
         items.append([item, options])
            
      else:
         print("NO ES DOUBLE SELECT")
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
   
   if Validationjs.objects.all().filter(question_id = question_id).exists():
      val = Validationjs.objects.get(question_id = question_id)
      validation = dict(validation = [val.name, val.value, val.condition_type.symbol])
      question_metadata['validation'] = validation

   print("QUESTION METADATA")
   print(question_metadata)
   json_question_metadata = json.dumps(question_metadata)
   ctx = {}
   ctx['company'] = company
   ctx['items'] = items
   ctx['template_type'] = template_type
   ctx['question_metadata'] = json_question_metadata
   print(ctx)
   return ctx