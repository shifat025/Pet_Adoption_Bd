from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import forms
from . import models

# Create your views here.
@login_required
def addpet(request):
    if request.method == 'POST':
        pet_form = forms.Petform(request.POST, request.FILES)
        if pet_form.is_valid():
            pet = pet_form.save(commit=False)
            pet.user = request.user  # Associate the current user with the pet
            pet.save()
            messages.success(request, 'Successfully Added')
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
    messages.success(request,"Deleted Successfully")
    return redirect('home')