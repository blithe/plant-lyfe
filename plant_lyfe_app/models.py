from django.db import models

class Plant(models.Model):
    common_name = models.CharField(max_length=200)
    subclass = models.CharField(max_length=200)
    order = models.CharField(max_length=200)
    family = models.CharField(max_length=200)
    genus = models.CharField(max_length=200)
    species = models.CharField(max_length=200)
