from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from pet.models import pets
from .models import Adopt
from transaction.models import account
from pet.models import pets
from transaction.views import send_email
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def adopt_history(request):
    data = Adopt.objects.filter(user=request.user)
    return render(request,'Authentication/adopt_history.html',{'dataa':data})


@login_required
def adopt(request, id):
    data = pets.objects.get(pk=id)
    useraccount = request.user.account
    available = data.is_available
    price = data.price
    balance = useraccount.account_balance

    if balance > price and available:
        balance -= price
        useraccount.account_balance = balance
        useraccount.save()
        data.save()
        buy=Adopt.objects.create(user=request.user, a_pets=data)
        send_email(request.user,price, "Adopt Message", "pet/adopt_mail.html")  
        return redirect('adopt_history')
    messages.warning(request, 'You donot have enough balanace to adopt it')
    return render(request,'Authentication/adopt_history.html',{'pet':data})