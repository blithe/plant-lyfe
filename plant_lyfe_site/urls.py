from django.conf.urls import patterns, include, url

from plant_lyfe_app.models import Plant

from rest_framework import serializers, viewsets, routers

from django.contrib import admin
admin.autodiscover()

import plant_lyfe_app.views

# Serializers define the API representation.
class PlantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plant
        fields = ('id', 'common_name', 'subclass', 'order', 'family', 'genus', 'species')

# ViewSets define the view behavior.
class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'dicots', PlantViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'plant_lyfe_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include(router.urls)),
    url(r'^index', plant_lyfe_app.views.index, name='index'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)
