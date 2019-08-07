from datetime import datetime
from django.shortcuts import render
from django.views import View
from jedzonko.models import Recipe


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)



def recipe_add(request):

    if request.method == "GET":
        return render(request, "app-add-recipe.html")
    else:
        name = request.POST.get("name")
        ingredients = request.POST.get("ingredients")
        description = request.POST.get("description")
        preparation_time = request.POST.get("preparation_time")
        instructions = request.POST.get("instructions")
        Recipe.objects.create(name=name, ingredients=ingredients,
                                       preparation_time=preparation_time, instructions=instructions, description=description)
    return render(request, "app-add-recipe.html")