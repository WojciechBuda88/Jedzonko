from django.db import models


# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.IntegerField()
    votes = models.IntegerField(default=0)
    instructions = models.TextField(null=True)

    def __str__(self):
        return self.name


class DayName(models.Model):
    day_name = models.CharField(max_length=16)
    order = models.IntegerField()

    def __str__(self):
        return self.day_name


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.CharField(max_length=255)

    def __str__(self):
        return {self.description}


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=255)
    order = models.IntegerField()
    day_name_id = models.ForeignKey(DayName, on_delete=models.CASCADE, related_name='recipe_plans')
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='recipe_plans')
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_plans')

    def __str__(self):
        return f'{self.plan_id} {self.day_name_id} {self.meal_name}'
