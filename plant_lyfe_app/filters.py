import django_filters
from plant_lyfe_app.models import Leaf

class LeafFilter(django_filters.FilterSet):

    class Meta:
        model = Leaf
        fields = ['id', 'plant', 'placement', 'blade', 'veins', 'location', 'date_found']
