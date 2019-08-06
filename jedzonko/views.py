from datetime import datetime

from django.shortcuts import render
from django.views import View

from jedzonko.models import Recipe


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class RecipeList(View):

    def get(self, request):
        recipes = Recipe.objects.all()
        return render(request, "recipes.html", context={"recipes": recipes})