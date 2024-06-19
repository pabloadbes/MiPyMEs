from .models import Item, Option

def ctx_dict(request):
   print("**********************************************************")
   print("**********************************************************")
   print("**********************************************************")
   print("**********************************************************")
   print("**********************************************************")
   print("**********************************************************")
   print("**********************************************************")

   ctx = {}
   
   aux = request.__str__().split("/")
   if aux[1] != "questions":
      return ctx

   question_number = aux[2]
   question_type = aux[3]
   template_type = temp_type(question_type)

   items = []
   its = Item.objects.all().filter(question_id = question_number)
   
   for item in its:
      opts = Option.objects.all().filter(item_id = item)
      options = []

      for option in opts:
         options.append(option)   

      items.append([item, options])
      
      
   ctx['items'] = items
   ctx['template_type'] = template_type
   print(ctx)
   return ctx

# question types
# 1:text
# 2:number
# 3:scale
# 4:select
# 5:multiple select

def temp_type(question_type):
   if question_type == '1':
      return './question_detail_type_text.html'
   elif question_type == '2':
      return './question_detail_type_number.html'
   elif question_type == '3':
      return './question_detail_type_scale.html'
   elif question_type == '4':
      return './question_detail_type_select.html'
   elif question_type == '5':
      return './question_detail_type_multiple.html'