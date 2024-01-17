from django.shortcuts import render,redirect
from pet.models import pet_category,pets
from pet.forms import ReviewForm
from buy.views import adopt
from buy.models import Adopt
from django.views.generic import DetailView
from django.http import HttpResponseForbidden


def home(request, pet_slug = None):
    data = pets.objects.all()
    if pet_slug is not None:
        pet_c = pet_category.objects.get(slug = pet_slug)
        data = pets.objects.filter(pet_type = pet_c)
    pet = pet_category.objects.all()
    return render(request, 'home.html', {'data': data, 'pet': pet})

class Details(DetailView):
    model = pets  # assuming 'pets' is the name of the model, change if necessary
    pk_url_kwarg = 'id'
    template_name = 'pet_details.html'
    context_object_name = 'details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet_model = self.object
        # Check if the user has bought the specific pet
        has_adopted_pet = Adopt.objects.filter( a_pets=pet_model).exists()

        if has_adopted_pet:
            reviews = pet_model.review_set.all()
            review_form = ReviewForm()
        else:
            reviews = None
            review_form = None

        context['reviews'] = reviews
        context['review_form'] = review_form
        context['has_adopted_pet'] = has_adopted_pet

        return context

    def post(self, request, *args, **kwargs):
        pet_model = self.get_object()

        # Check if the user has adopted the specific pet
        if not Adopt.objects.filter(user=request.user, a_pets=pet_model).exists():
            return HttpResponseForbidden("You can only review pets you have adopted.")

        review_form = ReviewForm(data=self.request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.pett = pet_model  # Update the field name to match your model
            new_review.user = self.request.user
            new_review.save()

        return redirect('Details', pet_model.id)  # Redirect to the pet details page after posting the review