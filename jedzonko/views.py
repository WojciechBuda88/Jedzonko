from datetime import datetime
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views import View
from jedzonko.models import Recipe, Plan, DayName, RecipePlan, Page


class IndexView(View):
    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class RecipeListView(View):
    def get(self, request):
        recipes = Recipe.objects.all().order_by("id")
        paginator = Paginator(recipes, 2)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        page_numbers = range(1, recipes.paginator.num_pages + 1)
        context = {
            "recipes": recipes,
            "page_numbers": page_numbers
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

        if name and ingredients and description and preparation_time and instructions:
            Recipe.objects.create(name=name, ingredients=ingredients,
                                  preparation_time=preparation_time, instructions=instructions, description=description)
            return redirect('/recipe/list')
        else:
            message = "Wypełnij poprawnie wszystkie pola"
            return render(request, "app-add-recipe.html", context={"message": message})


class AboutView(View):
    def get(self, request):
        try:
            about = Page.objects.get(slug='about')
            return render(request, "about.html", context={"about": about})
        except:
            message = "Strona w przygotowaniu"
            return render(request, "about.html", context={"message": message})

class ContactView(View):
    def get(self, request):
        try:
            contact = Page.objects.get(slug='contact')
            contact_detail = contact.description.split(",")
            return render(request, "contact.html", context={"contact_detail": contact_detail})
        except:
            message = "Strona w przygotowaniu"
            return render(request, "contact.html", context={"message": message})


class AppView(View):
    def get(self, request):
        plan_gty = Plan.objects.count()
        recipe_qty = Recipe.objects.count()
        plan_latest = Plan.objects.order_by('-created')[0]
        recipe_plans = plan_latest.recipe_plans.filter(plan_id=plan_latest.id).order_by('day_name_id', 'order')
        days = {}
        for recipe_plan in recipe_plans:
            day_name = recipe_plan.day_name_id.day_name
            if day_name not in days:
                days[day_name] = [recipe_plan]
            else:
                days[day_name].append(recipe_plan)

        context = {"plan_qty": plan_gty,
                   "recipe_qty": recipe_qty,
                   'plan': plan_latest,
                   'recipe_plans': recipe_plans,
                   'days': days,
                   }
        return render(request, 'dashboard.html', context=context)



class PlanAddView(View):
    def get(self, request):
        return render(request, 'app-add-schedules.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        new_plan = Plan.objects.create(name=name, description=description)
        request.session['plan_id'] = new_plan.id
        return redirect('/plan/add/details')


class PlanListView(View):
    def get(self, request):
        plans = Plan.objects.all().order_by('name')
        paginator = Paginator(plans, 2)
        page = request.GET.get('page')
        plans = paginator.get_page(page)
        page_numbers = range(1, plans.paginator.num_pages + 1)
        context = {
            'plans': plans,
            'page_numbers': page_numbers
        }
        return render(request, 'app-schedules.html', context=context)


class PlanDetailsView(View):
    def get(self, request, plan_id):
        plan = Plan.objects.get(pk=plan_id)
        recipe_plans = plan.recipe_plans.filter(plan_id=plan_id).order_by('day_name_id', 'order')
        days = {}
        for recipe_plan in recipe_plans:
            day_name = recipe_plan.day_name_id.day_name
            if day_name not in days:
                days[day_name] = [recipe_plan]
            else:
                days[day_name].append(recipe_plan)

        if recipe_plans and days:
            context = {
                'plan': plan,
                'recipe_plans': recipe_plans,
                'days': days,
            }
            return render(request, 'app-details-schedules.html', context=context)
        else:
            context = {
                'plan': plan,
                'message': 'Brak przepisów'
            }
            return render(request, 'app-details-schedules.html', context=context)


class RecipeDetailsView(View):
    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(pk=recipe_id)
        ingredients = recipe.ingredients.split(',')
        context = {
            'recipe': recipe,
            'ingredients': ingredients
        }
        return render(request, 'app-recipe-details.html', context=context)


class PlanEditView(View):
    def get(self, request):
        # if not request.session.get('plan_id'):
        #     raise Http404
        # return render(request, 'app-schedules-meal-recipe.html')
        days = DayName.objects.all()
        all_plans = Plan.objects.all()
        recipes = Recipe.objects.all()

        plan_id = request.session.get('plan_id')
        if plan_id:
            plan = Plan.objects.get(pk=plan_id)
            context = {
                'plan': plan,
                'all_plans': all_plans,
                'days': days,
                'recipes': recipes,
            }
        else:
            context = {
                'all_plans': all_plans,
                'days': days,
                'recipes': recipes,
            }
        return render(request, 'app-schedules-meal-recipe.html', context=context)

    def post(self, request):
        plan_id = request.session.get('plan_id')
        if plan_id:
            plan = Plan.objects.get(pk=plan_id)
        else:
            plan_id = request.POST.get('plan')
            plan = Plan.objects.get(pk=plan_id)

        all_plans = Plan.objects.all()

        meal_name = request.POST.get('meal_name')
        order = request.POST.get('order')

        day_name_id = request.POST.get('day_name_id')
        day = DayName.objects.get(pk=day_name_id)

        recipe_id = request.POST.get('recipe_id')
        recipe = Recipe.objects.get(pk=recipe_id)

        RecipePlan.objects.create(meal_name=meal_name, order=order, day_name_id=day, plan_id=plan,
                                  recipe_id=recipe)

        days = DayName.objects.all()
        recipes = Recipe.objects.all()
        context = {
            'plan': plan,
            'all_plans': all_plans,
            'days': days,
            'recipes': recipes,
        }
        return render(request, 'app-schedules-meal-recipe.html', context=context)


class RecipesView(View):
    def get(self, request):
        return render(request, 'recipes.html')


class RecipeNewView(View):
    def get(self, request):
        recipe = Recipe.objects.order_by('-created')[0]
        ingredients = recipe.ingredients.split(",")
        return render(request, 'app-recipe-details.html', context={"recipe": recipe, "ingredients": ingredients})


class RecipeModifyView(View):
    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        name = recipe.name
        ingredients = recipe.ingredients
        description = recipe.description
        preparation_time = recipe.preparation_time
        instructions = recipe.instructions
        return render(request, "app-add-recipe.html", context={'name': name, 'ingredients': ingredients,
                                                               'preparation_time': preparation_time,
                                                               'instructions': instructions,
                                                               'description': description})

    def post(self, request, recipe_id):
        recipe = Recipe.objects.get(pk=recipe_id)
        recipe.name = request.POST.get("name")
        recipe.ingredients = request.POST.get("ingredients")
        recipe.preparation_time = request.POST.get("preparation_time")
        recipe.instructions = request.POST.get("instructions")
        recipe.description = request.POST.get("description")

        if recipe.name and recipe.ingredients and recipe.description and recipe.preparation_time and recipe.instructions:
            recipe.save()
            message = "Przepis zaktualizowany"
            return render(request, "app-add-recipe.html", context={"message": message})
        else:
            message = "Wypełnij poprawnie wszystkie pola"
            return render(request, "app-add-recipe.html",
                          context={'name': recipe.name, 'ingredients': recipe.ingredients,
                                   'preparation_time': recipe.preparation_time,
                                   'instructions': recipe.instructions,
                                   'description': recipe.description,
                                   'message': message})


class PlanModifyView(View):
    def get(self, request, plan_id):
        plan = Plan.objects.get(pk=plan_id)
        context = {
            'plan': plan
        }
        return render(request, 'app-edit-schedules.html', context=context)

    def post(self, request, plan_id):
        plan = Plan.objects.get(pk=plan_id)
        plan.name = request.POST.get('name')
        plan.description = request.POST.get('description')
        if plan.name and plan.description:
            plan.save()
            return redirect('/plan/list')
        else:
            message = 'Błędne dane!'
            return render(request, 'app-edit-schedules.html', context={'message': message})


class PlanDeleteView(View):
    def get(self, request, plan_id):
        plan = Plan.objects.get(pk=plan_id)
        plan.delete()
        return redirect('/plan/list')


class RecipeDeleteView(View):
    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(pk=recipe_id)
        recipe.delete()
        return redirect('/recipe/list')


class RecipePlanDeleteView(View):
    def get(self, request, recipe_plan_id):
        recipe_plan = RecipePlan.objects.get(pk=recipe_plan_id)
        recipe_plan.delete()
        return redirect('/plan/list')


class PlanNewDetailsView(View):
    def get(self, request):
        if request.session.get('plan_id'):
            del request.session['plan_id']
        return redirect('/plan/list')
