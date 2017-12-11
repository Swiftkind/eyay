from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


User = get_user_model()

class Bot(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
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


class Knowledge(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    statement = models.CharField(max_length=100, blank=False)
    answer = models.TextField(blank=False)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return '{} bot knowledge'.format(self.bot)
