from django.db import models

class OnBoard(models.Model):
    image = models.ImageField(upload_to='static', height_field=None, width_field=None, max_length=100) 
    text = models.CharField(max_length=255)
    next_button = models.BooleanField()
