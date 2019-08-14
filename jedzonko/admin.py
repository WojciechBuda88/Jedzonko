from django.contrib import admin
from jedzonko.models import Recipe, Page, Plan, RecipePlan, DayName

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Page)
admin.site.register(Plan)
admin.site.register(RecipePlan)
admin.site.register(DayName)
