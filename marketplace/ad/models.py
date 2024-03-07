from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete

from user.models import CustomUser


class Category(models.TextChoices):
    AUTO = 'Auto'
    CLOTHING = 'Clothing'
    FOOTWEAR = 'Footwear'
    ACCESSORIES = 'Accessories'
    HOBBIES = 'Hobbies'
    PETS = 'Pets'
    SALE = 'Sale'
    SERVICES = 'Services'
    ELECTRONICS = 'Electronics'
    CHILDREN_GOODS = 'Children Goods'
    BEAUTY_HEALTH = 'Beauty and Health'
    OTHER = 'Other'


class Ad(models.Model):

    title = models.CharField(max_length=200, default='', blank=False)
    description = models.TextField(max_length=1000, default='', blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.OTHER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class AdImages(models.Model):

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, null=True, related_name='images')
    image = models.ImageField(upload_to='ad/images')

    def __str__(self):
        return self.ad.title

@receiver(post_delete, sender = AdImages)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)