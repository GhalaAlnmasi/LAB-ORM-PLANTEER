from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Plant,  Comment
from .forms import PlantForm,CommentForm

# Create your views here.

# All Plants
def plants_view(request:HttpRequest):
  # If no filters are applied, show all plants
  plants = Plant.objects.all().order_by('-created_at')
  # Filter by category if provided
  category = request.GET.get('category')
  if category:
      plants = plants.filter(category=category)

  # Filter by edibility if provided
  is_edible = request.GET.get('is_edible')
  if is_edible:
      plants = plants.filter(is_edible=is_edible.lower() == 'true')

  categories = Plant.Category.choices  # Get all category choices for the dropdown
  return render(request, 'plants/all_plants.html', {'plants': plants, 'categories': categories})

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
      plants = Plant.objects.filter(
          Q(name__icontains=query) | Q(about__icontains=query)
      )
      search_mode = True
  else:
      plants = Plant.objects.all()
      search_mode = False

  return render(request, 'plants/search_plant.html', {
      'plants': plants,
      'query': query,
      'search_mode': search_mode
  })