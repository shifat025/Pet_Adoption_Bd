from django import forms
from .models import Subscription1,Subscription2,Subscription3

class SubscribeForm_1(forms.ModelForm):
    class Meta:
        model = Subscription1
        fields = ['Month']

class SubscribeForm_2(forms.ModelForm):
    class Meta:
        model = Subscription2
        fields = ['Month']

class SubscribeForm_3(forms.ModelForm):
    class Meta:
        model = Subscription3
        fields = ['Month']