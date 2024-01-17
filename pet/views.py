from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from . import forms
from . import models

# Create your views here.
@login_required
def addpet(request):
    if request.method == 'POST':
        pet_form = forms.Petform(request.POST, request.FILES)
        if pet_form.is_valid():
            pet_form.save()
            return redirect('addpet')
        
    else:
        pet_form = forms.Petform()
    return render(request,'pet/add.html',{'form': pet_form})



@login_required
def pet_edit(request, id):
    posts = models.pets.objects.get(pk=id)
    p_edit_form = forms.Petform(instance=posts)
    if request.method == 'POST':
        p_edit_form = forms.Petform(request.POST, instance=posts)
        if p_edit_form.is_valid():
            p_edit_form.save()
            return redirect('home')
    return render(request, 'pet/add.html', {'form' : p_edit_form})
@login_required
def delete(request,id):
    posts = models.pets.objects.get(pk=id)
    posts.delete()
    return redirect('home')