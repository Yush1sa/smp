from django.db import models

# Create your models here.
class Projects(models.Model):
    title = models.TextField()
    
    dbeg = models.DateField()
    dend = models.DateField()
