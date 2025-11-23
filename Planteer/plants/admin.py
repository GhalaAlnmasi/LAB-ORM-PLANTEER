from django.contrib import admin
from .models import Plant
# Register your models here.


class PlantsAdmin(admin.ModelAdmin):
  list_display = ('name', 'about', 'native_to', 'used_for', 'category', 'is_edible')
  list_filter = ('category','is_edible', )
  list_editable = ('category',)
  

admin.site.register(Plant, PlantsAdmin)