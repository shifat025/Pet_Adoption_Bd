from django import forms
from .models import account

class AccountForm(forms.ModelForm):
    class Meta:
        model = account
        fields = ['diposit']