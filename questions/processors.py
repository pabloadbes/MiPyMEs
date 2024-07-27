from .models import Question, Item, Option, Note, Subsection
from companies.models import Company
from surveys.models import Survey

def ctx_dict(request):
   ctx = {}
   
   page = page_request(request)
   if page == "home":
      return ctx
   elif page == "questions":
      ctx = ctx_questions(request)
   elif page == "surveys":
      ctx = ctx_surveys(request)
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
   question_number = aux[2]
   question = Question.objects.get(id = question_number)
   survey_id = aux[3]
   company_id = Survey.objects.get(id = survey_id).company_id
   company = Company.objects.get(id = company_id)
   template_type = "./question_detail_type_" + question.question_type.__str__() + ".html"

   # subsection = Subsection.objects.all().filter(question_id = question_number).first()
   items = []
   its = Item.objects.all().filter(question_id = question_number)

   for item in its:
      opts = Option.objects.all().filter(item_id = item)
      options = []
      for option in opts:
         nts = Note.objects.all().filter(option_id = option.id)
         notes = []
         for note in nts:
            notes.append(note.text)
         options.append([option, notes])   
      items.append([item, options])

   ctx = {}
   ctx['company'] = company
   ctx['items'] = items
   ctx['template_type'] = template_type
   # if subsection:
      # ctx['subsection'] = subsection
   return ctx

def ctx_surveys(request):
   ctx = {}
   aux = request.__str__().split("/")
   if aux[2] == "init":
      if aux[3]:
         survey_id = int(''.join([car for car in aux[3] if car.isdigit()]))      
         survey = Survey.objects.get(id = survey_id)
         first_letter = survey.survey_type.name[0:1]
         ctx['first_letter'] = first_letter
         return ctx
   return ctx