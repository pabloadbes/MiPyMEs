from .models import Question, Item, Option

def ctx_dict(request):
   print("**********************************************************")
   print("**********************************************************")
   print("**********************************************************")
   print("**********************************************************")
   print("**********************************************************")
   print("**********************************************************")
   print("**********************************************************")

   ctx = {}
   
   page = page_request(request)
   print(page)
   if page == "home":
      return ctx
   elif page == "questions":
      ctx = ctx_questions(request)

   print(ctx)
   return ctx

# question types
# 1:text
# 2:number
# 3:scale
# 4:select
# 5:multiple select

def page_request(request):
   print(request)
   aux = request.__str__().split("/")
   print(aux)
   print(len(aux))
   if (aux[1]=="'>"):
      return "home"
   else:
      return aux[1]
   
def ctx_questions(request):
   aux = request.__str__().split("/")
   question_number = aux[2]
   question = Question.objects.all().filter(id = question_number).first()
   print(question)
   print(question.question_type)
   template_type = "./question_detail_type_" + question.question_type.__str__() + ".html"
   items = []
   its = Item.objects.all().filter(question_id = question_number)

   for item in its:
      opts = Option.objects.all().filter(item_id = item)
      options = []
      for option in opts:
         options.append(option)   
      items.append([item, options])

   ctx = {}
   ctx['items'] = items
   ctx['template_type'] = template_type
   return ctx
