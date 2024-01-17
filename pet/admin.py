from django.contrib import admin
from . import models

# Register your models here.
class pet_category_Admin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display=['name','slug']

admin.site.register(models.pet_category,pet_category_Admin) 

class pet_admin(admin.ModelAdmin):
    list_display=['name','pet_type','price','is_available']

admin.site.register(models.pets,pet_admin) 

class review_admin(admin.ModelAdmin):
    list_display=['ratting','comment']

admin.site.register(models.Review,review_admin) 