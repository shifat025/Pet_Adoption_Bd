from django.urls import path
from . import views

urlpatterns = [
    path('adopt/<int:id>/', views.adopt, name='adopt'),
    path('adopt_history',views.adopt_history,name='adopt_history'),
    path('Basic_subscribe/', views.subscribe_1, name='basic_subscribe'),
    path('Basic_subscribe_history/', views.subscribe_info, name='subscribe_his'),
    path('Standard_subscribe/',views.subscribe_2, name = 'standard_subscribe'),
    path('Premium_subscribe/',views.subscribe_3, name = 'premium_subscribe'),
    path('paypal-return/<str:subscription_type>/', views.paypal_return, name='paypal_return'),
    path('paypal-cancel/<str:subscription_type>/', views.paypal_cancel, name='paypal_cancel'),
     path('paypal-return/adopt/<int:id>/', views.paypal_return, {'subscription_type': 'adopt'}, name='paypal_return'),
    path('paypal-cancel/adopt/<int:id>/', views.paypal_cancel, {'subscription_type': 'adopt'}, name='paypal_cancel'),

]