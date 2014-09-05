from django.conf.urls import patterns, include, url

from plant_lyfe_app.models import Plant
from plant_lyfe_app.models import Leaf

from rest_framework import serializers, viewsets
from rest_framework_nested import routers

from django.contrib import admin
admin.autodiscover()

import plant_lyfe_app.views

# Serializers define the API representation.
class PlantSerializer(serializers.HyperlinkedModelSerializer):
    leaves = serializers.SlugRelatedField(many=True, slug_field='url')

    class Meta:
        model = Plant
        fields = ('id', 'common_name', 'subclass', 'order', 'family', 'genus', 'species', 'leaves')

    def plant_name(self, obj):
      return "plant-%(name)s" % {"name": obj.id}

class LeafSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaf
        fields = ('id', 'plant', 'placement', 'date_found')

# ViewSets define the view behavior.
class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

class LeafViewSet(viewsets.ModelViewSet):
    queryset = Leaf.objects.all()
    serializer_class = LeafSerializer


# Routers provide a way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'dicots', PlantViewSet)

dicots_router = routers.NestedSimpleRouter(router, r'dicots', lookup='dicots')
dicots_router.register(r'leaf', LeafViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'plant_lyfe_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include(router.urls)),
    url(r'^', include(dicots_router.urls)),
    url(r'^index', plant_lyfe_app.views.index, name='index'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)
