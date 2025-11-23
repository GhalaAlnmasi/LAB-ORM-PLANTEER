from django.db import models

# Create your models here.


class Country(models.Model):
  name = models.CharField(max_length=100, unique=True)
  flag = models.ImageField(upload_to='flags/')

  def __str__(self):
      return self.name
class Plant(models.Model):

  class Category(models.TextChoices):
    TREE = "tree", "Tree"                       # شجرة
    SHRUB = "shrub", "Shrub"                    # شجيرة
    SUBSHRUB = "subshrub", "Subshrub"           # شجيرة صغيرة
    HERB = "herb", "Herb"                       # نبات عشبي
    GRAMINOID = "graminoid", "Graminoid"        # نباتات نجيلية (Grass/Sedge/Rush)
    VINE = "vine", "Vine"                       # متسلق
    PALM = "palm", "Palm"                       # نخيل
    CACTUS = "cactus", "Cactus"                 # صباريات
    AQUATIC_FLOATING = "aquatic_floating", "Floating Aquatic Plant"     # نبات مائي طافٍ


  name = models.CharField(max_length=100)
  about = models.TextField()
  used_for = models.TextField()
  image = models.ImageField(upload_to='plants/images/')
  category =models.CharField(max_length=50, choices=Category.choices)
  is_edible = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  native_countries = models.ManyToManyField(Country, related_name='plants', blank=True)

  def __str__(self) -> str:
    return f"{self.name} from {self.category}"
  

class Comment(models.Model):
  plant = models.ForeignKey(
      Plant,
      on_delete=models.CASCADE,
      related_name="comments"
  )
  name = models.CharField(max_length=100)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return f"Comment by {self.name} on {self.plant.name}"