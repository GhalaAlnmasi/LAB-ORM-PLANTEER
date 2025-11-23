from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.db.models import Count
from .models import Plant, Country
from .forms import PlantForm,CommentForm

# Create your views here.

# All Plants
def plants_view(request:HttpRequest):
  # Get all plants
  plants_qs = Plant.objects.all().order_by('-created_at')

  # Apply filters
  context = filter_plants(request, queryset=plants_qs)
  
  return render(request, 'plants/all_plants.html', context)

# Add New Plants
def add_plant_view(request:HttpRequest):
  if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save()
            messages.success(request, f"Plant '{plant.name}' added successfully.")
            print("seccess")
            return redirect('plants:add_plant_view')
        else:
            print(form.errors)
  else:
      form = PlantForm()
  return render(request, 'plants/add_plant.html', {'form': form})

# Plants Details
def plant_details_view(request:HttpRequest, plant_id):
  plant = get_object_or_404(Plant, id=plant_id)
  comments = plant.comments.all().order_by('-created_at')

  if request.method == "POST":
      form = CommentForm(request.POST)
      if form.is_valid():
          comment = form.save(commit=False)
          comment.plant = plant
          comment.save()
          messages.success(request, "Your comment was added.")
          return redirect("plants:plant_details_view", plant_id=plant.id)
  else:
      form = CommentForm()

  # Get related plants based on the same category
  related_plants = Plant.objects.filter(category=plant.category).exclude(id=plant.id)[:4]  # Limit to 4 related plants
  return render(request, 'plants/plant_details.html', {'plant': plant, 'related_plants': related_plants, 'comments': comments,'form': form})

# Update Plants
def update_plant_view(request:HttpRequest, plant_id):
  plant = get_object_or_404(Plant, id=plant_id)
  if request.method == 'POST':
      form = PlantForm(request.POST, request.FILES, instance=plant)
      if form.is_valid():
          plant = form.save()
          messages.success(request, f"Plant '{plant.name}' updated successfully.")
          return redirect('plants:plant_details_view', plant_id=plant.id)
  else:
      form = PlantForm(instance=plant)
  return render(request, 'plants/update_plant.html', {'form': form, 'plant': plant})

# Delete Plants
def delete_plant(request:HttpRequest, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == "POST":
        plant_name = plant.name
        plant.delete()
        messages.success(request, f"Plant '{plant.name}' deleted successfully.")
        return redirect('plants:plants_view')

    return redirect(request.META.get('HTTP_REFERER', '/'))

# Search In Plants
def search_view(request:HttpRequest):
  query = request.GET.get('q', '').strip()
  if query:
      plants_qs = Plant.objects.filter(
          Q(name__icontains=query) | Q(about__icontains=query)
      )
      search_mode = True
  else:
      plants_qs = Plant.objects.all()
      search_mode = False
  
  context = filter_plants(request, queryset=plants_qs)
  context.update({
      'query': query,
      'search_mode': search_mode
  })

  return render(request, 'plants/search_plant.html', context)

def filter_plants(request, queryset=None):
  """
  Returns filtered plants based on GET parameters:
  - category
  - is_edible
  - native_countries (multiple)
  """

  if queryset is None:
      queryset = Plant.objects.all()

  # Apply category filter
  category = request.GET.get('category')
  if category:
      queryset = queryset.filter(category=category)

  # Apply edibility filter
  is_edible = request.GET.get('is_edible')
  if is_edible:
      queryset = queryset.filter(is_edible=is_edible.lower() == 'true')

  # Apply countries filter
  country_ids = request.GET.getlist('native_countries')
  if country_ids:
      queryset = queryset.filter(native_countries__id__in=country_ids)\
                          .annotate(num_countries=Count('native_countries'))\
                          .filter(num_countries=len(country_ids))

  # Prepare context data
  categories = Plant.Category.choices
  countries = Country.objects.all()
  selected_countries = country_ids

  return {
      'plants': queryset,
      'categories': categories,
      'countries': countries,
      'selected_countries': selected_countries
  }