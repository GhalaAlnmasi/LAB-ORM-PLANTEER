from django.contrib import admin
from .models import Plant,Country
# Register your models here.

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'flag')

class PlantsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('native_countries',)  # makes selection easier

admin.site.register(Plant, PlantsAdmin)