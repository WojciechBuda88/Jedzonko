from datetime import datetime
import random

from django.shortcuts import render
from django.views import View
from jedzonko.models import Recipe


class IndexView(View):
    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class RecipeListView(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        return render(request, "recipes.html", context={"recipes": recipes})

      
class MainView(View):
    def get(self, request):
        recipes = list(Recipe.objects.all())
        random.shuffle(recipes)
        context = {
            'recipes': recipes
        }
        return render(request, 'index.html', context=context)
      

def recipe_add(request):
    if request.method == "GET":
        return render(request, "recipe_add.html")
    else:
        name = request.POST.get("name")
        ingredients = request.POST.get("ingredients")
        description = request.POST.get("description")
        preparation_time = request.POST.get("preparation_time")
        instructions = request.POST.get("instructions")
        recipe = Recipe.objects.create(name=name, ingredients=ingredients,
                                       preparation_time=preparation_time, instructions=instructions, description=description)
        message = "Dodano nowy przepis!"
    return render(request, "recipe_add.html", context={"message":message})
  
  
class AboutView(View):
    def get(self, request):
        return render(request, "app_about.html")
      

class ContactView(View):
    def get(self, request):
        return render(request, "contact.html")

