from django.db import models
from django.contrib.auth.models import User

# Create your models here.
ratting = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')]


class pet_category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100,unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

class pets(models.Model):
    name = models.CharField( max_length=50)
    pet_type = models.ForeignKey(pet_category, on_delete=models.CASCADE)
    discription = models.TextField()
    image = models.FileField(upload_to='pet/media/uploads', blank = True, null = True)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pett = models.ForeignKey(pets, on_delete=models.CASCADE)
    ratting = models.CharField( max_length=50, choices=ratting)
    comment = models.TextField()

    def __str__(self):
        return self.ratting