from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from pet.models import pets
from .models import Adopt,Subscription1,Subscription2,Subscription3,Basic_subscription_history
from transaction.models import account
from pet.models import pets
from transaction.views import send_email
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.
@login_required
def adopt_history(request):
    data = Adopt.objects.filter(user=request.user)
    return render(request,'Authentication/adopt_history.html',{'dataa':data})

@login_required
def subscribe_history(request):
    data = Basic_subscription_history.objects.filter(user=request.user)
    print(data)
    return render(request,'Authentication/profile.html',{'s_data':data})



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
        messages.success(request,"Adopted Successfully")
        buy=Adopt.objects.create(user=request.user, a_pets=data)
        send_email(request.user,price, "Adopt Message", "pet/adopt_mail.html")  
        return redirect('adopt_history')
    messages.warning(request, 'You donot have enough balanace to adopt it')
    return render(request,'Authentication/adopt_history.html',{'pet':data})



@login_required
def subscribe_1(request):
    if request.method == 'POST':
        subscribe_form = forms.SubscribeForm_1(request.POST)

        if subscribe_form.is_valid():
            selected_month = subscribe_form.cleaned_data.get('Month')  # Use cleaned_data to get form field values
            subs = subscribe_form.save(commit=False)
            subs.user = request.user  # Associate the current user with the pet
            subs.save()

            price = subs.subcribe_price * int(selected_month)
            useraccount = request.user.account
            balance = useraccount.account_balance

            if balance >= price:
                balance -= price
                useraccount.account_balance = balance
                useraccount.save()

                # Uncomment this line if you want to store subscription information in the database
                # subscription = Subscription1.objects.create(user=request.user, Month=selected_month)
                result = subs.subcribe_price * selected_month
                messages.success(request, "Subscribed Successfully")

                # Uncomment and adjust this line based on your email sending implementation
                # send_email(request.user, price, "Subscription Message", "path/to/subscription_mail.html")

                return redirect('Subscription_his')

            messages.warning(request, 'You do not have enough balance to subscribe.')
    else:
        subscribe_form = forms.SubscribeForm_1()  # Instantiate the form without request.POST

    return render(request, 'Authentication/subscribe.html', {'subscribe_form': subscribe_form })


@login_required
def subscribe_2(request):
    if request.method == 'POST':
        subscribe_form = forms.SubscribeForm_2(request.POST)

        if subscribe_form.is_valid():
            selected_month = subscribe_form.cleaned_data.get('Month')  # Use cleaned_data to get form field values
            subs = subscribe_form.save(commit=False)
            subs.user = request.user  # Associate the current user with the pet
            subs.save()

            price = subs.subcribe_price * int(selected_month)
            useraccount = request.user.account
            balance = useraccount.account_balance

            if balance >= price:
                balance -= price
                useraccount.account_balance = balance
                useraccount.save()

                # Uncomment this line if you want to store subscription information in the database
                # subscription = Subscription1.objects.create(user=request.user, Month=selected_month)

                messages.success(request, "Subscription Successfully")

                # Uncomment and adjust this line based on your email sending implementation
                # send_email(request.user, price, "Subscription Message", "path/to/subscription_mail.html")

                return redirect('subscribe_his')

            messages.warning(request, 'You do not have enough balance to subscribe.')
    else:
        subscribe_form = forms.SubscribeForm_2()  # Instantiate the form without request.POST

    return render(request, 'Authentication/subscribe.html', {'subscribe_form': subscribe_form})

@login_required
def subscribe_3(request):
    if request.method == 'POST':
        subscribe_form = forms.SubscribeForm_3(request.POST)

        if subscribe_form.is_valid():
            selected_month = subscribe_form.cleaned_data.get('Month')  # Use cleaned_data to get form field values
            subs = subscribe_form.save(commit=False)
            subs.user = request.user  # Associate the current user with the pet
            subs.save()

            price = subs.subcribe_price * int(selected_month)
            useraccount = request.user.account
            balance = useraccount.account_balance

            if balance >= price:
                balance -= price
                useraccount.account_balance = balance
                useraccount.save()

                # Uncomment this line if you want to store subscription information in the database
                # subscription = Subscription1.objects.create(user=request.user, Month=selected_month)

                messages.success(request, "Subscription Successfully")

                # Uncomment and adjust this line based on your email sending implementation
                # send_email(request.user, price, "Subscription Message", "path/to/subscription_mail.html")
                
                return redirect('subscribe_his')

            messages.warning(request, 'You do not have enough balance to subscribe.')
    else:
        subscribe_form = forms.SubscribeForm_3()  # Instantiate the form without request.POST

    return render(request, 'Authentication/subscribe.html', {'subscribe_form': subscribe_form})

@login_required
def subscribe_info(request):
    subscriptions1 = Subscription1.objects.all()
    subscriptions2 = Subscription2.objects.all()
    subscriptions3 = Subscription3.objects.all()
    
    all_subscriptions = {
        'subscriptions1': subscriptions1,
        'subscriptions2': subscriptions2,
        'subscriptions3': subscriptions3,
    }
    for subscription in subscriptions1:
        subscription.result = subscription.subcribe_price * subscription.Month
    for subscription in subscriptions2:
        subscription.result = subscription.subcribe_price * subscription.Month
    for subscription in subscriptions3:
        subscription.result = subscription.subcribe_price * subscription.Month
    
    return render(request, 'Authentication/subscribe_history.html', {'datas': all_subscriptions})
