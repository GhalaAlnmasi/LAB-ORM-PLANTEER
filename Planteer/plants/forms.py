from django import forms
from .models import Plant, Comment

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'about', 'native_to', 'used_for', 'image', 'category', 'is_edible']
        widgets = {
            'about': forms.Textarea(attrs={'rows': 3}),
            'used_for': forms.Textarea(attrs={'rows': 2}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content']