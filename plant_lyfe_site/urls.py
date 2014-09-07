from django.conf.urls import patterns, include, url

from plant_lyfe_app.models import Plant, Leaf

from django.http import Http404

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

import code

from django.contrib import admin
admin.autodiscover()

# Serializers define the API representation.
class PlantListSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SerializerMethodField('label_id')
    leaves = serializers.RelatedField(many=True)

    class Meta:
        model = Plant
        fields = ('id', 'common_name', 'species', 'leaves')

    def label_id(self, obj):
      return "plant-" + str(obj.id)

class PlantSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SerializerMethodField('label_id')
    leaves = serializers.RelatedField(many=True)

    class Meta:
        model = Plant
        fields = ('id', 'common_name', 'subclass', 'order', 'family', 'genus', 'species', 'leaves')

    def label_id(self, obj):
      return "plant-" + str(obj.id)

class LeafSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('label_id')
    plant = serializers.RelatedField()

    class Meta:
        model = Leaf
        fields = ('id', 'plant', 'placement', 'blade', 'veins', 'location', 'date_found')

    def label_id(self, obj):
      return "leaf-" + str(obj.id)


# ViewSets define the view behavior.
class PlantList(APIView):

    def get(self, request, format=None):
        plants = Plant.objects.all()
        serializer = PlantListSerializer(plants, many=True)
        return Response({'plants': serializer.data})

    def post(self, request, format=None):
        serializer = PlantSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlantDetail(APIView):

    def get_object(self, slug):
        try:
            return Plant.objects.get(slug=slug)
        except Plant.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        plant = self.get_object(slug)
        serializer = PlantSerializer(plant)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        serializer = PlantSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, slug, format=None):
      plant = self.get_object(slug)
      serializer = PlantSerializer(plant, data=request.DATA, partial=True)
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        plant = self.get_object(slug)
        plant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LeafDetail(APIView):

    def get_plant_object(self, plant_slug):
        try:
            return Plant.objects.get(slug=plant_slug)
        except Plant.DoesNotExist:
            raise Http404

    def get_object(self, plant_slug, pk):
        plant = self.get_plant_object(plant_slug)
        try:
            return plant.leaves.get(pk=pk)
        except Leaf.DoesNotExist:
            raise Http404

    def get(self, request, plant_slug, pk, format=None):
        leaf = self.get_object(plant_slug, pk)
        serializer = LeafSerializer(leaf)
        return Response(serializer.data)

    def post(self, request, plant_slug, pk, format=None):
        leaf = self.get_object(plant_slug, pk)
        serializer = LeafSerializer(leaf, data=request.DATA, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, plant_slug, pk, format=None):
        leaf = self.get_object(plant_slug, pk)
        leaf.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'plant_lyfe_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^dicots/$', PlantList.as_view()),
    url(r'^dicots/(?P<slug>[\w-]+)/$', PlantDetail.as_view()),
    url(r'^dicots/(?P<plant_slug>[\w-]+)/leaf/(?P<pk>\d+)/$', LeafDetail.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)
