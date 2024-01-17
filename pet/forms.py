from django import forms
from .models import Review,pets,pet_category


class Petform(forms.ModelForm):
    class Meta:
        model = pets
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['ratting', 'comment']