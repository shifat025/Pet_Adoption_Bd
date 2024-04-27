from django.urls import path
from . import views

urlpatterns = [
    path('sing_up/', views.sing_up, name='sing_up'),
    path('login/', views.Loginview.as_view(), name='user_login'),
    path('profile/Update', views.UpdateView.as_view(), name='Profile_update'),
    path('profile/password_change/', views.pass_change, name='pass_change'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact_view, name='contact'),
    path('email_verification/<str:uidb64>/<str:token>/', views.EmailVerificationView.as_view(), name='email_verification'),
 
]