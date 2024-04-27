from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from transaction.models import account
from .models import ContactMessage


class SingForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        
    def save(self, commit=True):
            our_user = super().save(commit=False) # ami database e data save korbo na ekhn
            if commit == True:
                our_user.save() # user model e data save korlam
                account.objects.create(user = our_user)
                return our_user
            return our_user

class ChangeUserForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']