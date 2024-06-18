from .models import Item, Option

def ctx_dict(request):
   print("**********************************************************")
   print("**********************************************************")
   print("**********************************************************")
   print("**********************************************************")
   print("**********************************************************")
   print("**********************************************************")
   print("**********************************************************")
   aux = request.__str__().split("/")
   question_number = aux[2]
   question_type = aux[3]
   ctx = {}
   items = []
   options = []

   its = Item.objects.all().filter(question_id = question_number)
   
   for item in its:
      opts = Option.objects.all().filter(item_id = item)
      list_aux = []

      for option in opts:
         list_aux.append(option.text)   
      items.append(item.text+"wwwww")
      options.append(list_aux)
      items.append("idjsfoisjfoijdof")
      
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