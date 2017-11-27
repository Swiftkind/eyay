from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


User = get_user_model()

class Bot(models.Model):
    AUTOMOTIVE = 'AU'
    CLOTHING = 'CL'
    SOFTWARE = 'SO'
    CATEGORY_CHOICES = (
        (AUTOMOTIVE, 'Automotive'),
        (CLOTHING, 'Clothing'),
        (SOFTWARE, 'Software')
    )

    name = models.CharField(max_length=50)
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default=AUTOMOTIVE,
    )
    is_active = models.BooleanField(default=True)
    tags = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Separate tags with commas. Ex: python,django,flask'
    )
    creator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='creator'
    )

    def __str__(self):
        return self.name
