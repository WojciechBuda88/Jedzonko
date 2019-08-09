"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from jedzonko.views import IndexView, AboutView, ContactView, RecipeListView, RecipeAddView, MainView, AppView, \
    PlanAddView, PlanListView, PlanDetailsView, RecipeDetailsView, RecipesView, RecipeNewView, PlanEditView, \
    RecipeModifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view()),
    path('main/', AppView.as_view()),

    path('', MainView.as_view()),

    path('recipe/add/', RecipeAddView.as_view(), name="recipe_add"),
    path('recipe/list/', RecipeListView.as_view()),
    path('recipe/<int:recipe_id>/', RecipeDetailsView.as_view()),

    path('plan/add/', PlanAddView.as_view()),
    path('plan/list/', PlanListView.as_view()),
    path('plan/<int:plan_id>/', PlanDetailsView.as_view()),

    path('plan/add/details', PlanEditView.as_view()),

    path('recipes/', RecipesView.as_view()),

    path('about/', AboutView.as_view()),
    path('contact/', ContactView.as_view()),
    path('new_recipe/', RecipeNewView.as_view()),
    path('recipe/modify/<int:recipe_id>', RecipeModifyView.as_view()),
]

