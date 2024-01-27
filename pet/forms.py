from django import forms
from .models import Review,pets,pet_category


class Petform(forms.ModelForm):
    class Meta:
        model = pets
        fields = ['name','pet_type','discription','image','is_available','price']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['ratting', 'comment']