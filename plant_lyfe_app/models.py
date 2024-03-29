from django.db import models
from django.template.defaultfilters import slugify

class Plant(models.Model):
    common_name = models.CharField(max_length=200)
    subclass = models.CharField(max_length=200)
    order = models.CharField(max_length=200)
    family = models.CharField(max_length=200)
    genus = models.CharField(max_length=200)
    species = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.common_name)
        super(Plant, self).save(*args, **kwargs)

    def __unicode__(self):
        return "plant-" + str(self.id)

class Leaf(models.Model):
    plant = models.ForeignKey(Plant, related_name='leaves')
    placement = models.CharField(max_length=200)
    blade = models.CharField(max_length=200)
    veins = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    date_found = models.DateField('date-found')

    def __unicode__(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        return "/dicots/%s/leaf/%i" % (self.plant.slug, self.id)
