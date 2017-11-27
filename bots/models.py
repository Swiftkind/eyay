from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


User = get_user_model()

class Bot(models.Model):
    CATEGORY_CHOICES = (
        (1, 'Automotive'),
        (2, 'Clothing'),
        (3, 'Software')
    )

    name = models.CharField(max_length=50)
    category = models.IntegerField(
        choices=CATEGORY_CHOICES,
        default=1,
    )
    is_active = models.BooleanField(default=True)
    tags = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Separate tags with commas. Ex: python,django,flask'
    )
    created = models.DateField(auto_now=True)
    creator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='creator'
    )

    def __str__(self):
        return self.name
