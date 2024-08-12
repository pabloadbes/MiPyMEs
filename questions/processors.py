from .models import Question, Item, Option, Note, Subsection
from companies.models import Company
from surveys.models import Survey, Variable_List

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

   items = []
   its = Item.objects.all().filter(question_id = question_id)
   for item in its:
      opts = Option.objects.all().filter(item_id = item)
      options = []
      for option in opts:
         nts = Note.objects.all().filter(option_id = option.id)
         notes = []
         for note in nts:
            notes.append(note.text)
         if option.children:
            child_items = []
            print("TIENE HIJO")
            child_its = Item.objects.all().filter(id = option.children.id)
            print(child_its)
            for child_item in child_its:
               child_options = []
               child_opts = Option.objects.all().filter(item_id = child_item.id)
               print(child_opts)
               for child_option in child_opts:
                  print(child_option)
                  child_options.append(child_option)
               child_items.append([child_item, child_options])
            options.append([option, notes, child_items])
         else:
            options.append([option, notes])   
      items.append([item, options])

   ctx = {}
   ctx['company'] = company
   ctx['items'] = items
   ctx['template_type'] = template_type
   return ctx