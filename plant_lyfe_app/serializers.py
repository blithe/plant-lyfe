from rest_framework import serializers
from plant_lyfe_app.models import Plant, Leaf


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
