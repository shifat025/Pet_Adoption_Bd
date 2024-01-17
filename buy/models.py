from django.db import models
from django.contrib.auth.models import User
from pet.models import pets

# Create your models here.

class Adopt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    a_pets = models.ForeignKey(pets, on_delete=models.CASCADE,null=True)
    adopt_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username