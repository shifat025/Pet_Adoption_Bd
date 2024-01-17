from django.urls import path
from . import views

urlpatterns = [
    path('addpet/', views.addpet, name='addpet'),
    path('pet_edit/<int:id>/', views.pet_edit, name='pet_edit'),
    path('delete/<int:id>', views.delete, name='delete'),
  
 
]