from datetime import datetime
import random

from django.shortcuts import render
from django.views import View
from jedzonko.models import Recipe, Plan


class IndexView(View):
    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class RecipeListView(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        context = {
            "recipes": recipes
        }
        return render(request, "app-recipes.html", context=context)


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
        Recipe.objects.create(name=name, ingredients=ingredients,
                              preparation_time=preparation_time, instructions=instructions, description=description)
        return render(request, "app-add-recipe.html")


class AboutView(View):
    def get(self, request):
        return render(request, "about.html")


class ContactView(View):
    def get(self, request):
        return render(request, "contact.html")


class AppView(View):
    def get(self, request):
        return render(request, 'dashboard.html')


class PlanAddView(View):
    def get(self, request):
        return render(request, 'app-add-schedules.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        Plan.objects.create(name=name, description=description)
        return render(request, 'app-add-schedules.html')


class PlanListView(View):
    def get(self, request):
        plans = Plan.objects.all().order_by('name')
        context = {
            'plans': plans
        }
        return render(request, 'app-schedules.html', context=context)


class PlanDetailsView(View):
    def get(self, request, plan_id):
        plan = Plan.objects.get(pk=plan_id)
        recipe_plans = plan.recipe_plans.filter(plan_id=plan_id).order_by('day_name_id', 'order')
        context = {
            'plan': plan,
            'recipe_plans': recipe_plans
        }
        return render(request, 'app-details-schedules.html', context=context)
