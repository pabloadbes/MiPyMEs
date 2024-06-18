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

   items = []
   options = []

   its = Item.objects.all().filter(question_id = question_number)
   
   for item in its:
      opts = Option.objects.all().filter(item_id = item)
      list_aux = []

      for option in opts:
         list_aux.append(option)   
      items.append(item)
      options.append(list_aux)
      
   ctx['items'] = items
   ctx['options'] = options
   print(ctx)
   return ctx

# question types
# 1:text
# 2:number
# 3:scale
# 4:select
# 5:multiple select