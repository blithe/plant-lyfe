from django.shortcuts import render
from django.http import Http404

from plant_lyfe_app.serializers import PlantListSerializer, PlantSerializer, LeafSerializer
from plant_lyfe_app.models import Plant, Leaf

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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
