from django.db import models
from django.contrib.auth.models import User
from pet.models import pets

# Create your models here.
month = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10')]
subscription_choices = [
        ('Basic', 'Basic'),
        ('Standard', 'Standard'),
        ('Premium', 'Premium'),
        # Add more subscription types if needed
    ]

class Adopt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    a_pets = models.ForeignKey(pets, on_delete=models.CASCADE,null=True)
    adopt_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Subscription1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subcribe_price = models.IntegerField(default=49)
    subscription = models.CharField(default='Basic', choices=subscription_choices, max_length=20)
    Month = models.IntegerField(choices=[(i, str(i)) for i in range(1, 13)])            
    subscription_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.user.username
    
class Subscription2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subcribe_price = models.IntegerField(default=99)
    subscription = models.CharField(default='Standard', choices=subscription_choices, max_length=20)
    Month = models.IntegerField(choices=[(i, str(i)) for i in range(1, 13)])
    subscription_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.user.username

    
class Subscription3(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subcribe_price = models.IntegerField(default=149)
    subscription = models.CharField(default='Premium', choices=subscription_choices, max_length=20)
    Month = models.IntegerField(choices=[(i, str(i)) for i in range(1, 13)])
    subscription_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.user.username
    
class Basic_subscription_history(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    a_subscription = models.ForeignKey(Subscription1, on_delete=models.CASCADE,null=True)
    adopt_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username