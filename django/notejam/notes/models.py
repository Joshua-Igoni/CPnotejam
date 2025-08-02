from django.db import models
from pads.models import Pad
from django.contrib.auth.models import User


class Note(models.Model):
    pad = models.ForeignKey(Pad, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
