from datetime import datetime
import random

from django.shortcuts import render
from django.views import View
from jedzonko.models import Recipe


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class MainView(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        context = {
            'recipes': random.choices(recipes, k=3)
        }
        return render(request, 'index.html', context=context)
