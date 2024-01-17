from django.shortcuts import render,redirect
from . import forms
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views import View
from .forms import ChangeUserForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from pet.models import pets
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def sing_up(request):
    if request.method == 'POST':
        sing_up_form = forms.SingForm(request.POST)
        if sing_up_form.is_valid():
            user = sing_up_form.save()
            user.is_active = False
            user.save()

            # Send email verification
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('Authentication/veryfication_mail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, 'Account Created Successfully. Please check your email to activate your account.')
            return redirect('user_login')

    else:
        sing_up_form = forms.SingForm()
    return render(request, 'Authentication/register.html', {'form': sing_up_form, 'type': 'sing_up'})

class EmailVerificationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Email verification successful. You can now log in.')
        else:
            messages.error(request, 'Email verification failed.')
        return HttpResponse("Email verification completed. You can close this tab.")



class Loginview(LoginView):
    template_name = 'Authentication/register.html'
    def get_success_url(self):
        return reverse_lazy('profile')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successful')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.success(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context

@login_required
def user_logout(request):
    logout(request)
    messages.success(request,'Logged Out Successfully')
    return redirect('user_login')

@login_required
def profile(request):
     
    return render(request,'Authentication/profile.html' )


class UpdateView(View,LoginRequiredMixin):
    template_name = 'authentication/profile_update.html'

    def get(self, request):
        form = ChangeUserForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ChangeUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})
    
@login_required
def pass_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Updated Successfully')
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'Authentication/pass_change.html', {'form' : form})