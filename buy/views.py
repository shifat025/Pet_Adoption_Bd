from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from pet.models import pets
from .models import Adopt,Subscription1,Subscription2,Subscription3,Basic_subscription_history
from pet.models import pets
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import forms
from .paypal_payment import create_paypal_payment
import paypalrestsdk

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
    # Get the pet data
    data = pets.objects.get(pk=id)
    available = data.is_available
    price = data.price

    if available:
        # If the user has enough balance, create a PayPal payment
        return_url = request.build_absolute_uri(f'/paypal-return/adopt/{id}/')
        cancel_url = request.build_absolute_uri(f'/paypal-cancel/adopt/{id}/')

        payment_url = create_paypal_payment(price, f"Adopt {data.name} for {request.user.username}", return_url, cancel_url)

        if payment_url:
            # If PayPal payment URL is created, redirect the user to PayPal
            return redirect(payment_url)
        else:
            messages.error(request, "An error occurred during PayPal payment creation.")
            return redirect('adopt_history')

    else:
        # If balance is insufficient or pet is not available
        messages.warning(request, 'You do not have enough balance to adopt this pet or the pet is no longer available.')
        return redirect('adopt_history')





@login_required
def subscribe_1(request):
    if request.method == 'POST':
        subscribe_form = forms.SubscribeForm_1(request.POST)
        if subscribe_form.is_valid():
            selected_month = subscribe_form.cleaned_data.get('Month')
            subs = subscribe_form.save(commit=False)
            subs.user = request.user
            subs.save()

            total_price = subs.subcribe_price * int(selected_month)

            # Dynamic return URL for subscribe_1
            return_url = request.build_absolute_uri(f'/paypal-return/1/')
            cancel_url = request.build_absolute_uri(f'/paypal-cancel/1/')
            
            payment_url = create_paypal_payment(total_price, f"Basic subscription for {request.user.username} ({selected_month} months)", return_url, cancel_url)

            if payment_url:
                return redirect(payment_url)
            else:
                messages.error(request, "An error occurred during PayPal payment creation.")
                return redirect('basic_subscribe')

    else:
        subscribe_form = forms.SubscribeForm_1()

    return render(request, 'Authentication/subscribe.html', {'subscribe_form': subscribe_form})



@login_required
def subscribe_2(request):
    if request.method == 'POST':
        subscribe_form = forms.SubscribeForm_2(request.POST)
        if subscribe_form.is_valid():
            selected_month = subscribe_form.cleaned_data.get('Month')
            subs = subscribe_form.save(commit=False)
            subs.user = request.user
            subs.save()
            price = subs.subcribe_price * int(selected_month)
            return_url = request.build_absolute_uri('/paypal-return/2/')
            cancel_url = request.build_absolute_uri('/paypal-cancel/2/')
            payment_url = create_paypal_payment(price, f"Standard subscription for {request.user.username} ({selected_month} months)", return_url, cancel_url)

            if payment_url:
                return redirect(payment_url)
            else:
                messages.error(request, "An error occurred during PayPal payment creation.")
                return redirect('standard_subscribe')
    else:
        subscribe_form = forms.SubscribeForm_2()

    return render(request, 'Authentication/subscribe.html', {'subscribe_form': subscribe_form})


@login_required
def subscribe_3(request):
    if request.method == 'POST':
        subscribe_form = forms.SubscribeForm_3(request.POST)
        if subscribe_form.is_valid():
            selected_month = subscribe_form.cleaned_data.get('Month')
            subs = subscribe_form.save(commit=False)
            subs.user = request.user
            subs.save()
            price = subs.subcribe_price * int(selected_month)
            return_url = request.build_absolute_uri('/paypal-return/3/')
            cancel_url = request.build_absolute_uri('/paypal-cancel/3/')
            payment_url = create_paypal_payment(price, f"Premium subscription for {request.user.username} ({selected_month} months)", return_url, cancel_url)

            if payment_url:
                return redirect(payment_url)
            else:
                messages.error(request, "An error occurred during PayPal payment creation.")
                return redirect('premium_subscribe')
    else:
        subscribe_form = forms.SubscribeForm_3()

    return render(request, 'Authentication/subscribe.html', {'subscribe_form': subscribe_form})



@login_required
def paypal_return(request, subscription_type=None, id=None):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    # Find the payment by its ID
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        if subscription_type == 'adopt':  # Handle adoption payments
            pet = get_object_or_404(pets, pk=id)
            if not pet.is_available:
                messages.error(request, f"{pet.name} is no longer available.")
                return redirect('adopt_history')

            # Save adoption record
            Adopt.objects.create(user=request.user, a_pets=pet)
            # pet.is_available = False
            pet.save()

            messages.success(request, "Adoption successful!")
            return redirect('adopt_history')
        else:
            # Handle other subscriptions (Basic, Standard, Premium)
            if subscription_type == '1':  # Basic Subscription
                messages.success(request, "Your payment was successful! Basic subscription activated.")
                return redirect('subscribe_his')
            elif subscription_type == '2':  # Standard Subscription
                messages.success(request, "Your payment was successful! Standard subscription activated.")
                return redirect('subscribe_his')
            elif subscription_type == '3':  # Premium Subscription
                messages.success(request, "Your payment was successful! Premium subscription activated.")
                return redirect('subscribe_his')
    else:
        messages.error(request, "Payment execution failed.")
        return redirect('home')  # Redirect to home if payment failed

@login_required
def paypal_cancel(request, subscription_type=None, id=None):
    if subscription_type == 'adopt':
        if id:
            messages.warning(request, "You canceled the adoption payment.")
            return redirect('Details', id=id)  # Redirect back to the specific pet adoption page
        else:
            messages.warning(request, "You canceled the adoption payment.")
            return redirect('adopt_history')  # Fallback if no pet ID is provided
    elif subscription_type == '1':
        messages.warning(request, "You canceled the payment for the Basic subscription.")
        return redirect('basic_subscribe')
    elif subscription_type == '2':
        messages.warning(request, "You canceled the payment for the Standard subscription.")
        return redirect('standard_subscribe')
    elif subscription_type == '3':
        messages.warning(request, "You canceled the payment for the Premium subscription.")
        return redirect('premium_subscribe')
    else:
        messages.warning(request, "Payment process was canceled.")
        return redirect('home')  # Generic fallback redirect

    


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


