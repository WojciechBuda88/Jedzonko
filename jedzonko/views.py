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


class RecipeAddView(View):
    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request):
        name = request.POST.get("name")
        ingredients = request.POST.get("ingredients")
        description = request.POST.get("description")
        preparation_time = request.POST.get("preparation_time")
        instructions = request.POST.get("instructions")

        if name and ingredients and description and preparation_time and instructions:
            Recipe.objects.create(name=name, ingredients=ingredients,
                                  preparation_time=preparation_time, instructions=instructions, description=description)
            return render(request, "app-add-recipe.html")
        else:
            message = "Wypełnij poprawnie wszystkie pola"
            return render(request, "app-add-recipe.html", context={"message":message})



class AboutView(View):
    def get(self, request):
        return render(request, "about.html")


class ContactView(View):
    def get(self, request):
        return render(request, "contact.html")
