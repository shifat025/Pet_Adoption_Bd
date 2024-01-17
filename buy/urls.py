from django.urls import path
from . import views

urlpatterns = [
    path('adopt/<int:id>/', views.adopt, name='adopt'),
    path('adopt_history',views.adopt_history,name='adopt_history')
   
]