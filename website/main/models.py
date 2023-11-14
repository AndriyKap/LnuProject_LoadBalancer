from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BellTask(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(null=True, default=None) 
    result = models.CharField() 
    timestamp = models.DateTimeField(auto_now_add=True) 
    STATUS_CHOICES = [
        ('in progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in progress')